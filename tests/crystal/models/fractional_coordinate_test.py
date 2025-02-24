import pytest

from tda_crystallography.crystal.models.fractional_coordinate import FractionalCoordinate

class TestFractionalCoordinate:

    @pytest.fixture
    def fractional_coordinate(self) -> FractionalCoordinate:
        return FractionalCoordinate(x=-1/3, y=2, z=1.5)
    
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