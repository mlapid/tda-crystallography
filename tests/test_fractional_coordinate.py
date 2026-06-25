import pytest

from tda_crystallography.crystal.fractional_coordinate import FractionalCoordinate
from tda_crystallography.crystal.unit_cell import UnitCell


class TestFractionalCoordinate:
    @pytest.mark.parametrize(
        'c1, c2, expected',
        [
            (
                FractionalCoordinate(x=1 / 3, y=2, z=1.5),
                FractionalCoordinate(x=1 / 3, y=2, z=1.5),
                True,
            ),
            (
                FractionalCoordinate(x=-1.3, y=0, z=1.5),
                FractionalCoordinate(x=0.7, y=2, z=0.5),
                True,
            ),
            (
                FractionalCoordinate(x=1 / 3, y=2, z=1.5),
                FractionalCoordinate(x=-1 / 3, y=2, z=1.5),
                False,
            ),
        ],
    )
    def test_equality(self, c1: FractionalCoordinate, c2: FractionalCoordinate, expected: bool):
        assert (c1 == c2) is expected

    @pytest.mark.parametrize(
        'x, y, z, expected',
        [
            (-1.3, 0, 1.5, (0.7, 0.0, 0.5)),
            (2.0, 3.0, 4.0, (0.0, 0.0, 0.0)),
            (0.25, 0.5, 0.75, (0.25, 0.5, 0.75)),
        ],
    )
    def test_wraps_coordinates_to_unit_cell(
        self,
        x: float,
        y: float,
        z: float,
        expected: tuple[float, float, float],
    ):
        coordinate = FractionalCoordinate(x=x, y=y, z=z)
        assert (coordinate.x, coordinate.y, coordinate.z) == pytest.approx(expected)

    def test_orthogonalise(self):
        unit_cell = UnitCell(a=25.12, b=39.5, c=45.07, alpha=90, beta=90, gamma=90)
        coordinate = FractionalCoordinate(x=0.5, y=0.5, z=0.5)
        orthogonalised = coordinate.orthogonalise(unit_cell)

        assert (orthogonalised.x, orthogonalised.y, orthogonalised.z) == pytest.approx((
            12.56,
            19.75,
            22.535,
        ))

    def test_hashable_in_set(self):
        c1 = FractionalCoordinate(x=-1.3, y=0, z=1.5)
        c2 = FractionalCoordinate(x=0.7, y=2, z=0.5)

        assert {c1, c2} == {c1}
