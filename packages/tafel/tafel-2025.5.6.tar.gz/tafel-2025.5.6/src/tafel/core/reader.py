import re
from io import StringIO
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


class SimpleXYReader:
    def read_xy(self, path: str) -> None:
        self.df = pd.read_csv(path)

    def get_tafel_plots(self) -> list[tuple[np.ndarray, np.ndarray, str]]:
        return [(self.df["x"], self.df["y"], "")]


class Reader:
    def __init__(
        self,
        ph: float = 13,
        reference_potential: float = 0.210,
        electrolyte_resistance: float = 0.05,
    ) -> None:
        self.ph = ph
        self.reference_potential = reference_potential
        self.electrolyte_resistance = electrolyte_resistance

    def read_mpt(self, path: str) -> None:
        with Path(path).open() as f:
            contents = f.read()

        lines = contents.splitlines()
        metadata = {}

        for _, line in enumerate(lines):
            if line.startswith("mode"):
                break
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()

        self.docs = metadata

        header_line = metadata.get("Nb header lines", "0")
        header_lines = int(header_line)

        self.df = pd.read_csv(path, skiprows=header_lines - 1, sep="\t")

        electrode_surface_area = metadata.get("Electrode surface area", "0 cm2").split(" cm2")[0]
        self.electrode_surface_area = float(electrode_surface_area)

    def get_potential_shift(self) -> float:
        return self.ph * 0.0591 + self.reference_potential

    def get_log_j(self) -> np.ndarray:
        sdf = self.get_decent_data(self.df)
        return self.i_to_logj(sdf)

    def get_decent_data(self, df: pd.DataFrame) -> pd.DataFrame:
        mask = df["<I>/mA"] > 0
        return df.loc[mask, :].copy()

    def i_to_logj(self, df: pd.DataFrame) -> np.ndarray:
        return np.log10(df["<I>/mA"] / 1000 / self.electrode_surface_area)

    def get_tafel_plot(self) -> tuple:
        logj = self.get_log_j()
        ircp = self.get_ir_corrected_potential()

        return logj, ircp

    def get_ir_corrected_potential(self) -> np.ndarray:
        sdf = self.get_decent_data(self.df)
        return self.apply_ir_correction(sdf)

    def apply_ir_correction(self, df: pd.DataFrame) -> np.ndarray:
        potential_shift = self.get_potential_shift()
        e_vs_rhe_v = df["Ewe/V"] + potential_shift
        ia = df["<I>/mA"] / 1000
        ir = ia * self.electrolyte_resistance

        return (e_vs_rhe_v - ir).to_numpy()

    def get_tafel_plots(self) -> list[tuple[np.ndarray, np.ndarray, str]]:
        plt = self.get_tafel_plot()
        return [(plt[0], plt[1], "")]


class HokutoReader(Reader):
    def get_number_of_measurements(self) -> int:
        return len(self.docs["measurements"])

    @staticmethod
    def txt_to_dict(txt: str) -> dict[str, Any]:
        sections = re.split(r"《(.*?)》\n", txt)[1:]

        # Parsing into a dictionary
        parsed_data = {}

        for i in range(0, len(sections), 2):
            section_name = sections[i].strip()
            section_content = sections[i + 1].strip().split("\n")

            if "測定データ" in section_name:
                # Handling measurement data separately
                data = pd.read_csv(StringIO("\n".join(section_content)), sep=",", header=None)
                data.columns = data.iloc[0]
                data = data.iloc[1:]
                parsed_data[section_name] = data
            else:
                # General key-value extraction
                section_dict = {}
                for line in section_content:
                    parts = [x.strip() for x in line.split(",") if x.strip()]
                    if len(parts) == 2:  # noqa: PLR2004
                        section_dict[parts[0]] = parts[1]
                    elif len(parts) > 2:  # noqa: PLR2004
                        section_dict[parts[0]] = parts[1:]  # Store as list if multiple values
                parsed_data[section_name] = section_dict

        return parsed_data

    def get_tafel_plots(self) -> list[tuple[np.ndarray, np.ndarray, str]]:
        measurements = []
        for kind in ["アノード", "カソード"]:
            for measurement in self.docs["measurements"]:
                _df = measurement["測定データ"]
                _df = _df.query(f"種別 == '{kind}'")
                _df = _df.rename(columns={"3 電流I": "<I>/mA", "4 WE/CE": "Ewe/V"})

                _df["<I>/mA"] = _df["<I>/mA"].astype(float)
                _df["Ewe/V"] = _df["Ewe/V"].astype(float)

                _df = self.get_decent_data(_df)

                logj = self.i_to_logj(_df)
                ircp = self.apply_ir_correction(_df)

                metadata = measurement.copy()

                del metadata["測定データ"]
                metadata["kind"] = kind
                name = f"{kind}-{metadata['測定フェイズヘッダ']['サイクル番号']}"

                measurements.append((logj, ircp, name))

        return measurements

    def read_csv(self, path: str) -> None:
        measurements = []
        self.docs = {}

        with Path(path).open(encoding="shift-jis") as f:
            contents = f.read()

        chapters = contents.split("《測定フェイズヘッダ》")

        for i, chapter in enumerate(chapters):
            if i == 0:
                self.docs["metadata"] = self.txt_to_dict(chapter)
            else:
                _docs = self.txt_to_dict("《測定フェイズヘッダ》" + chapter)
                measurements.append(_docs)

        self.docs["measurements"] = measurements
        # Splitting the sections

        self.df = self.docs["measurements"][-1]["測定データ"]

        self.df = self.df.rename(columns={"3 電流I": "<I>/mA", "4 WE/CE": "Ewe/V"})
        self.df["<I>/mA"] = self.df["<I>/mA"].astype(float)
        self.df["Ewe/V"] = self.df["Ewe/V"].astype(float)

        area_info = self.docs["metadata"]["測定情報"]["面積"]
        if area_info[1] == "cm2":
            self.electrode_surface_area = float(area_info[0])
        else:
            msg = f"Unknown area unit: {area_info[1]}"
            raise ValueError(msg)
