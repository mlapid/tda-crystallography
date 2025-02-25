import pytest

from tda_crystallography.crystal.models.unit_cell import UnitCell

class TestUnitCell:

    @pytest.fixture
    def unit_cell(self) -> UnitCell:
        return UnitCell(a=1, b=1, c=1, alpha=90, beta=90, gamma=90)
    
    def test_volume(self, unit_cell: UnitCell):
        assert unit_cell.volume == 1