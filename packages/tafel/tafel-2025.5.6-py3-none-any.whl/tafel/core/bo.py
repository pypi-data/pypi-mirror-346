from collections.abc import Callable
from pathlib import Path

import numpy as np
import optuna
import optuna.logging
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import linregress
from sklearn.metrics import r2_score

optuna.logging.set_verbosity(optuna.logging.WARNING)

ggplot_palette = [
    "#E41A1C",  # Red
    "#377EB8",  # Blue
    "#4DAF4A",  # Green
    "#984EA3",  # Purple
    "#FF7F00",  # Orange
    "#FFFF33",  # Yellow
    "#A65628",  # Brown
    "#F781BF",  # Pink
]


def objective_find_line(
    x: np.ndarray, y: np.ndarray, forbidden: list[int] | None = None
) -> Callable[[optuna.trial.Trial], tuple[float, int]]:
    """
    x: np.array. log10(j) (mA/cm2)
    y: np.array. V vs RHE (E-iR, V)
    forbidden: list[int]. Indices that are forbidden to be used in the line.
    """
    if forbidden is None:
        forbidden = []

    def objective(trial: optuna.trial.Trial) -> tuple[float, int]:
        # Suggest two indices for slicing the data, ensuring idx2 >= idx1
        idx1 = trial.suggest_int("i1", 0, len(x) - 3)
        idx2 = trial.suggest_int("i2", idx1 + 2, len(x))  # Ensure idx2 >= idx1

        n_points = idx2 - idx1

        # Forbidden range
        list1 = list(range(idx1, idx2))
        common_elements = set(list1).intersection(forbidden or [])

        # Check if there are common elements
        if common_elements:
            return 0.0, 0

        _x = x[idx1:idx2]
        _y = y[idx1:idx2]

        _x = np.array(_x)
        _y = np.array(_y)

        res = linregress(_x, _y)
        predictions = _x * res.slope + res.intercept  # type: ignore[attr-defined]
        r2: float = float(r2_score(_y, predictions))

        return r2, n_points

    return objective


def perform_bayesian_optimization(
    x: np.ndarray,
    y: np.ndarray,
    trials: int,
    r2_threshold: float,
    points_threshold: int,
    lines: int,
    forbidden_idxs: list[int],
) -> tuple[list[tuple[int, int, linregress]], list[optuna.study.Study]]:  # type: ignore[type-arg]
    fit_results = []
    studies = []
    old_studies: list[optuna.study.Study] = []

    for _i in range(lines):
        study = optuna.create_study(
            directions=["maximize", "maximize"],
            sampler=optuna.samplers.NSGAIISampler(seed=42),
        )

        for old_study in old_studies:
            for t in old_study.trials:
                # Forbidden range
                list1 = list(range(t.params["i1"] + 1, t.params["i2"]))
                common_elements = set(list1).intersection(forbidden_idxs)

                # Check if there are common elements
                values = (0, 0) if common_elements else t.values  # noqa: PD011

                study.add_trial(
                    optuna.trial.create_trial(params=t.params, values=values, distributions=t.distributions)
                )

        study.optimize(
            objective_find_line(x, y, forbidden=forbidden_idxs),
            n_trials=trials,
            timeout=300,
        )

        df_trials = study.trials_dataframe()
        df_trials = df_trials.query(f"values_1 > {points_threshold}")
        df_trials = df_trials.query(f"values_0 > {r2_threshold}")

        if df_trials.empty:
            continue

        max_entry = df_trials.sort_values(by=["values_1", "values_0"], ascending=[False, False]).iloc[0]
        i1 = int(max_entry["params_i1"])
        i2 = int(max_entry["params_i2"])

        _x = x[i1:i2]
        _y = y[i1:i2]
        res = linregress(_x, _y)

        fit_results.append((i1, i2, res))
        forbidden_idxs.extend(range(i1, i2))
        studies.append(study)
        old_studies.append(study)

    return fit_results, studies


class BayesianOptimizer:
    def __init__(
        self,
        trials: int,
        r2_threshold: float,
        points_threshold: int,
        lines: int,
        forbidden_idxs: list[int],
        output_dir: Path,
    ) -> None:
        self.trials = trials
        self.r2_threshold = r2_threshold
        self.points_threshold = points_threshold
        self.lines = lines
        self.forbidden_idxs = forbidden_idxs
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def fit(  # noqa: PLR0915
        self, x: np.ndarray, y: np.ndarray
    ) -> tuple[list[optuna.study.Study], list[tuple[int, int, linregress]]]:  # type: ignore[type-arg]
        tafel_fig = self.save_raw_data(x, y)

        fit_idxs = []
        forbidden_idxs: list[int] = []

        fit_results, studies = perform_bayesian_optimization(
            x=x,
            y=y,
            trials=self.trials,
            r2_threshold=self.r2_threshold,
            points_threshold=self.points_threshold,
            lines=self.lines,
            forbidden_idxs=forbidden_idxs,
        )

        for i, result in enumerate(fit_results):
            i1, i2, res = result
            _x = x[i1:i2]
            _y = y[i1:i2]

            filtered_x = _x[np.isfinite(_x)]  # This removes both inf and nan values

            x_min = np.nanmin(filtered_x)
            x_max = np.nanmax(filtered_x)

            x_range = np.linspace(x_min, x_max, 100)  # Generate 100 points for a smooth line
            y_line = res.slope * x_range + res.intercept

            # Select color from the palette
            color = ggplot_palette[i % len(ggplot_palette)]  # Cycle through the palette

            # Create a line trace
            line_trace = go.Scatter(
                x=x_range,
                y=y_line,
                mode="lines",
                name=f"{res.slope * 1000:.1f} meV/dec",
                line={"color": color},
            )
            fit_idxs.append((i1, i2))
            # Add the line trace to the existing figure
            tafel_fig.add_trace(line_trace)

            forbidden_idxs.extend(range(i1, i2))

        # Optionally, update layout if needed
        tafel_fig.data[0].marker.size = 4  # type: ignore[attr-defined]

        tafel_fig.write_image(self.output_dir / "optfit.png")
        tafel_fig.write_image(self.output_dir / "optfit.pdf")
        for study_i, (study, result) in enumerate(zip(studies, fit_results, strict=True)):
            i1, i2, res = result

            df_study = study.trials_dataframe()
            df_study["is_best"] = (df_study.params_i1 == i1) & (df_study.params_i2 == i2)
            slopes = []
            intercepts = []
            x_mins = []
            x_maxs = []
            for _, row in df_study.iterrows():
                i1 = int(row["params_i1"])
                i2 = int(row["params_i2"])
                _x = x[i1:i2]
                _y = y[i1:i2]

                res = linregress(_x, _y)
                slopes.append(res.slope)  # type: ignore[attr-defined]
                intercepts.append(res.intercept)  # type: ignore[attr-defined]
                x_mins.append(np.min(_x))
                x_maxs.append(np.max(_x))

            df_study["slope"] = slopes
            df_study["intercept"] = intercepts
            df_study["xmin"] = x_mins
            df_study["xmax"] = x_maxs
            study_path = self.output_dir / f"study_{study_i}.csv"
            df_study.to_csv(study_path)

            df_study_r2_positive = df_study.query("values_0 > 0")
            line_trace = go.Scatter(
                x=df_study_r2_positive.number,
                y=df_study_r2_positive.values_0,
            )
            study_fig = go.Figure(data=[line_trace])
            study_fig.write_image(self.output_dir / f"study_r2_{study_i}.pdf")

            line_trace = go.Scatter(
                x=df_study_r2_positive.number,
                y=df_study_r2_positive.values_1,
            )
            study_fig = go.Figure(data=[line_trace])
            study_fig.write_image(self.output_dir / f"study_num_{study_i}.pdf")

            contour_fig = optuna.visualization.plot_contour(
                study=study,
                params=["i1", "i2"],
                target=lambda t: t.values[0],  # noqa: PD011
                target_name="R2",
            )
            contour_fig.update_layout(
                font={"family": "Helvetica", "size": 32},
                width=450,
                height=500,
                title="",
                xaxis={"title": ""},
                yaxis={"title": ""},
            )

            contour_fig.write_image(self.output_dir / f"contour_{study_i}-R2.png")
            contour_fig.write_image(self.output_dir / f"contour_{study_i}-R2.pdf")
            contour_fig = optuna.visualization.plot_contour(
                study=study,
                params=["i1", "i2"],
                target=lambda t: t.values[1],  # noqa: PD011
                target_name="n",
            )
            contour_fig.update_layout(
                font={"family": "Helvetica", "size": 32},
                width=550,
                height=500,
                title="",
                xaxis={"title": ""},
                yaxis={"title": ""},
            )
            contour_fig.write_image(self.output_dir / f"contour_{study_i}-n.pdf")

        return studies, fit_results

    def save_raw_data(self, x: np.ndarray, y: np.ndarray) -> go.Figure:
        trace = go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker={"size": 10, "color": "#999999"},
            line={"shape": "linear", "color": "rgba(0, 0, 255, 0.8)", "width": 2},
            hovertemplate="<b>%{x}, %{y}</b><br>ID: %{customdata}<extra></extra>",
            name="Raw data",
        )

        layout = go.Layout(
            title="Tafel Plot",
            xaxis={
                "title": "log j (A/cm2)",
                "gridcolor": "lightgray",
                "showgrid": True,
            },
            yaxis={
                "title": "Overpotential (V)",
                "gridcolor": "lightgray",
                "showgrid": True,
            },
            font={"family": "Roboto, sans-serif", "size": 18, "color": "black"},
            plot_bgcolor="white",
        )
        traces = [trace]

        tafel_fig = go.Figure(data=traces, layout=layout)

        tafel_fig.update_layout(
            autosize=False,  # Disable automatic sizing
            width=450,  # Set figure width
            height=500,  # Set figure height
            title=None,
            xaxis={
                "showgrid": False,  # Hide x-axis gridlines
                "linecolor": "black",  # X-axis line color
                "linewidth": 2,  # X-axis line width
                "mirror": True,  # Mirror axis line, creating a box effect
                "ticks": "outside",  # Ticks position
                "tickwidth": 2,  # Ticks width
                "tickcolor": "black",  # Ticks color
                "ticklen": 4,  # Ticks length
                "tickformat": ".1f",  # Use one decimal place for tick labels
            },
            yaxis={
                "showgrid": False,  # Hide y-axis gridlines
                "linecolor": "black",  # Y-axis line color
                "linewidth": 2,  # Y-axis line width
                "mirror": True,  # Mirror axis line, creating a box effect
                "ticks": "outside",  # Ticks position
                "tickwidth": 2,  # Ticks width
                "tickcolor": "black",  # Ticks color
                "ticklen": 4,  # Ticks length
                "tickformat": ".2f",  # Use one decimal place for tick labels
            },
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            paper_bgcolor="rgba(0,0,0,0)",  # Transparent surrounding paper
            font={
                "family": "Arial, sans-serif",  # Specify the font family here
                "size": 18,  # You can also set the font size
            },
        )

        tafel_fig.write_image(self.output_dir / "tafel_fig.png")

        raw_csv_path = self.output_dir / "x_y_data.csv"
        pd.DataFrame({"x": x, "y": y}).to_csv(raw_csv_path, index=False)

        return tafel_fig
