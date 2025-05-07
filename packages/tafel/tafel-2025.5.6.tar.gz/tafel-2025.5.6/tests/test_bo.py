import shutil
from pathlib import Path
from unittest import TestCase

from tafel.core.bo import BayesianOptimizer
from tafel.core.reader import HokutoReader, Reader


class TestBO(TestCase):
    def test_perform_bayesian_optimization(self):
        reader = Reader()
        reader.read_mpt("tests/data/example.mpt")
        x = reader.get_log_j()
        y = reader.get_ir_corrected_potential()
        bo = BayesianOptimizer(10, 0.5, 2, 1, [], Path("test_output"))
        bo.fit(x, y)
        bo = BayesianOptimizer(
            trials=10,
            r2_threshold=0.5,
            points_threshold=2,
            lines=2,
            forbidden_idxs=[],
            output_dir=Path("test_output"),
        )
        studies, fit_results = bo.fit(x, y)

        assert len(studies) == 2
        assert len(fit_results) == 2

    def tearDown(self):
        if Path("test_output").exists():
            shutil.rmtree("test_output")

    def test_bo_with_hokuto(self):
        reader = HokutoReader()
        reader.read_csv("tests/data/example2.CSV")

        x = reader.get_log_j()
        y = reader.get_ir_corrected_potential()
        bo = BayesianOptimizer(
            trials=10,
            r2_threshold=0.5,
            points_threshold=30,
            lines=1,
            forbidden_idxs=[],
            output_dir=Path("test_output"),
        )
        studies, fit_results = bo.fit(x, y)

        assert len(studies) == 1
        assert len(fit_results) == 1

    def test_measurements(self):
        reader = HokutoReader()
        reader.read_csv("tests/data/example2.CSV")

        assert reader.get_number_of_measurements() == 3

        for x, y, name in reader.get_tafel_plots():
            print(name)
            print(x)
            print(y)
            bo = BayesianOptimizer(
                trials=10,
                r2_threshold=0.01,
                points_threshold=3,
                lines=2,
                forbidden_idxs=[],
                output_dir=Path("test_output") / name,
            )
            bo.fit(x, y)
