import pytest

from tda_crystallography.crystal.positional_coordinate import PositionalCoordinate
from tda_crystallography.crystal.unit_cell import UnitCell


class TestPositionalCoordinate:
    @pytest.fixture
    def positional_coordinate(self) -> PositionalCoordinate:
        return PositionalCoordinate(x=-1 / 3, y=2.0, z=1.5)

    def test_equality(self, positional_coordinate: PositionalCoordinate):
        other = PositionalCoordinate(x=-1 / 3, y=2.0, z=1.5)
        assert positional_coordinate == other

    def test_inequality(self, positional_coordinate: PositionalCoordinate):
        other = PositionalCoordinate(x=1 / 3, y=2.0, z=1.5)
        assert positional_coordinate != other

    def test_allows_negative_and_zero_components(self):
        coordinate = PositionalCoordinate(x=-1.0, y=0.0, z=3.5)
        assert coordinate.x == -1.0
        assert coordinate.y == 0.0
        assert coordinate.z == 3.5

    def test_hashable_in_set(self, positional_coordinate: PositionalCoordinate):
        duplicate = PositionalCoordinate(x=-1 / 3, y=2.0, z=1.5)
        assert {positional_coordinate, duplicate} == {positional_coordinate}

    def test_is_frozen(self, positional_coordinate: PositionalCoordinate):
        with pytest.raises(Exception):
            positional_coordinate.x = 0.0

    def test_normalise_scales_coordinates(self, positional_coordinate: PositionalCoordinate):
        normalised = positional_coordinate.normalise(2.0)

        assert normalised == PositionalCoordinate(
            x=-2 / 3,
            y=4.0,
            z=3.0,
        )
        assert positional_coordinate == PositionalCoordinate(x=-1 / 3, y=2.0, z=1.5)

    def test_normalise_with_unit_cell_constant(self):
        unit_cell = UnitCell(a=25.12, b=39.5, c=45.07, alpha=90, beta=90, gamma=90)
        coordinate = PositionalCoordinate(x=12.56, y=19.75, z=22.535)

        normalised = coordinate.normalise(unit_cell.normalising_constant)

        assert normalised == PositionalCoordinate(
            x=0.3538519091782396,
            y=0.5564152234291586,
            z=0.6348768131633463,
        )

    @pytest.mark.parametrize('constant', [0, -1.0])
    def test_normalise_rejects_non_positive_constant(
        self,
        positional_coordinate: PositionalCoordinate,
        constant: float,
    ):
        with pytest.raises(ValueError, match='Normalising constant must be positive'):
            positional_coordinate.normalise(constant)