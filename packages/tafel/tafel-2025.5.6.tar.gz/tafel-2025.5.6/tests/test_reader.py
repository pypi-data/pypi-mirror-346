import pytest

from tafel.core.reader import HokutoReader, Reader, SimpleXYReader


class TestReader:
    def test_read_mpt(self):
        reader = Reader(ph=13.5, reference_potential=0.4, electrolyte_resistance=0.1)
        reader.read_mpt("tests/data/example.mpt")

        assert reader.electrode_surface_area == pytest.approx(0.45)
        assert reader.get_potential_shift() == pytest.approx(1.19785)

        logj, ircp = reader.get_tafel_plot()
        assert len(logj) == 327
        assert len(ircp) == 327

        assert max(logj) == pytest.approx(-3.83285168745084)
        assert min(logj) == pytest.approx(-6.20186542677148)
        assert max(ircp) == pytest.approx(2.3188025875739773)
        assert min(ircp) == pytest.approx(1.3191080925889032)

        print(reader.docs)
        assert reader.docs["Characteristic mass"] == "0.001 g"

    def test_read_hokuto(self):
        reader = HokutoReader()
        reader.read_csv("tests/data/example2.CSV")
        assert reader.electrode_surface_area == 1.0
        logj, ircp = reader.get_tafel_plot()

        assert len(reader.docs["measurements"]) == 3
        assert len(logj) == len(ircp)

        assert len(reader.get_tafel_plots()) == 6

    def test_read_xy(self):
        reader = SimpleXYReader()
        reader.read_xy("dataset/HER.xy")
        assert len(reader.get_tafel_plots()) == 6
