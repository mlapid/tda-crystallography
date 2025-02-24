import pytest

from tda_crystallography.crystal.coordinates.fractional_coordinate import FractionalCoordinate

class TestFractionalCoordinate:

    @pytest.fixture
    def fractional_coordinate(self) -> FractionalCoordinate:
        return FractionalCoordinate(x=-1/3, y=2, z=1.5)
    
    def test_wrap_to_unit(self, fractional_coordinate: FractionalCoordinate):
        assert (
            fractional_coordinate.x >= 0 and fractional_coordinate.x < 1 and \
            fractional_coordinate.y >= 0 and fractional_coordinate.y < 1 and \
            fractional_coordinate.z >= 0 and fractional_coordinate.z < 1
        )