import pytest

from tda_crystallography.crystal.models.positional_coordinate import PositionalCoordinate

class TestPositionalCoordinate:

    @pytest.fixture
    def positional_coordinate(self) -> PositionalCoordinate:
        return PositionalCoordinate(x=-1/3, y=2, z=1.5)