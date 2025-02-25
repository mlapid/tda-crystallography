import pytest

from tda_crystallography.crystal.models.unit_cell import UnitCell
from tda_crystallography.crystal.models.fractional_coordinate import FractionalCoordinate
from tda_crystallography.crystal.models.positional_coordinate import PositionalCoordinate

class TestFractionalCoordinate:
    
    @pytest.mark.parametrize('c1, c2, expected', [
        # Equal coordinates
        (
            FractionalCoordinate(x=1/3, y=2, z=1.5),
            FractionalCoordinate(x=1/3, y=2, z=1.5),
            True
        ),
        # Equal wrapped coordinates
        (
            FractionalCoordinate(x=-1.3, y=0, z=1.5),
            FractionalCoordinate(x=0.7, y=2, z=0.5),
            True
        ),
        # Different coordinates
        (
            FractionalCoordinate(x=1/3, y=2, z=1.5),
            FractionalCoordinate(x=-1/3, y=2, z=1.5),
            False
        )
    ])
    
    def test_equality(self, c1: FractionalCoordinate, c2: FractionalCoordinate, expected: bool):
        assert (c1 == c2) == expected

    def test_orthogonalisation(self):
        unit_cell = UnitCell(a=25.12, b=39.5, c=45.07, alpha=90, beta=90, gamma=90)
        coordinate = FractionalCoordinate(x=0.5, y=0.5, z=0.5)
        orthogonal_coordinate: PositionalCoordinate = coordinate.orthogonalise(unit_cell)
        assert orthogonal_coordinate == PositionalCoordinate(x=12.56, y=19.75, z=22.535)