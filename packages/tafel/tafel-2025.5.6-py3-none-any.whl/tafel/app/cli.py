import argparse

from tafel.core.bo import BayesianOptimizer
from tafel.core.reader import HokutoReader, Reader, SimpleXYReader


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True)
    parser.add_argument("-p", "--ph", type=float, default=13, help="pH of the electrolyte (default: 13)")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="tafel_plot",
        help="Output directory name (default: tafel_plot)",
    )
    parser.add_argument(
        "-t",
        "--trials",
        type=int,
        default=1000,
        help="Number of trials (default: 1000)",
    )
    parser.add_argument(
        "--r2-threshold",
        type=float,
        default=0.998,
        help="R2 threshold (default: 0.998)",
    )
    parser.add_argument("-l", "--lines", type=int, default=2, help="Number of lines (default: 2)")

    parser.add_argument(
        "-pt",
        "--points-threshold",
        type=int,
        default=5,
        help="Number of points threshold (default: 5)",
    )
    parser.add_argument(
        "-r",
        "--reference-potential",
        type=float,
        default=0.210,
        help="""Reference potential in V vs RHE (default: 0.210 V)
    Common choices:
        Standard hydrogen electrode (SHE): 0.0 V
        Saturated calomel electrode: 0.241 V
        Ag/AgCl/saturated KCl: 0.197 V
        Ag/AgCl/3.5 mol/kg KCl: 0.205 V
        Ag/AgCl/3.0 mol/kg KCl: 0.210 V
        Ag/AgCl/1.0 mol/kg KCl: 0.235 V
        Ag/AgCl/0.6 mol/kg KCl: 0.250 V
        Ag/AgCl (seawater): 0.266 V""",
    )
    parser.add_argument(
        "-e",
        "--electrolyte-resistance",
        type=float,
        default=0.05,
        help="Electrolyte resistance (default: 0.05)",
    )

    args = parser.parse_args()

    if ".mpt" in args.file:
        reader = Reader(
            ph=args.ph,
            reference_potential=args.reference_potential,
            electrolyte_resistance=args.electrolyte_resistance,
        )
        reader.read_mpt(args.file)

    elif ".csv" in args.file:
        reader = SimpleXYReader()
        reader.read_xy(args.file)
    elif ".CSV" in args.file:
        reader = HokutoReader(
            ph=args.ph,
            reference_potential=args.reference_potential,
            electrolyte_resistance=args.electrolyte_resistance,
        )
        reader.read_csv(args.file)
    else:
        raise NotImplementedError

    for x, y, name in reader.get_tafel_plots():
        opt = BayesianOptimizer(
            trials=args.trials,
            r2_threshold=args.r2_threshold,
            points_threshold=args.points_threshold,
            lines=args.lines,
            output_dir=args.output + f"/{name}",
            forbidden_idxs=[],
        )
        opt.fit(x=x, y=y)


if __name__ == "__main__":
    main()
