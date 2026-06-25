import numpy as np
import pytest
from pydantic import ValidationError

from tda_crystallography.crystal.unit_cell import UnitCell


class TestUnitCell:
    @pytest.fixture
    def unit_cell(self) -> UnitCell:
        return UnitCell(a=1, b=1, c=1, alpha=90, beta=90, gamma=90)

    def test_volume_of_unit_cube(self, unit_cell: UnitCell):
        assert unit_cell.volume == 1.0

    def test_volume_of_orthogonal_cell(self):
        unit_cell = UnitCell(
            a=13.6770,
            b=12.6070,
            c=18.4970,
            alpha=90.0,
            beta=90.0,
            gamma=90.0,
        )

        assert unit_cell.volume == pytest.approx(3189.362593683)

    def test_normalising_constant_of_unit_cube(self, unit_cell: UnitCell):
        assert unit_cell.normalising_constant == 1.0

    def test_normalising_constant_of_orthogonal_cell(self):
        unit_cell = UnitCell(a=25.12, b=39.5, c=45.07, alpha=90, beta=90, gamma=90)

        assert unit_cell.normalising_constant == pytest.approx(0.028172922705273853)

    def test_orthogonalisation_matrix_of_orthogonal_cell(self):
        unit_cell = UnitCell(a=25.12, b=39.5, c=45.07, alpha=90, beta=90, gamma=90)

        np.testing.assert_allclose(
            unit_cell.orthogonalisation_matrix,
            np.array([
                [25.12, 0.0, 0.0],
                [0.0, 39.5, 0.0],
                [0.0, 0.0, 45.07],
            ]),
            atol=1e-12,
        )

    def test_orthogonalisation_matrix_of_triclinic_cell(self):
        unit_cell = UnitCell(a=3, b=4, c=5, alpha=70, beta=80, gamma=75)

        np.testing.assert_allclose(
            unit_cell.orthogonalisation_matrix,
            np.array([
                [2.885005236929854, 0.0, 0.0],
                [0.636680120958634, 3.758770483143633, 0.0],
                [0.520944533000791, 1.368080573302675, 5.0],
            ]),
            atol=1e-12,
        )

    def test_equality(self, unit_cell: UnitCell):
        assert unit_cell == UnitCell(a=1, b=1, c=1, alpha=90, beta=90, gamma=90)

    def test_is_frozen(self, unit_cell: UnitCell):
        with pytest.raises(Exception):
            unit_cell.a = 2.0

    @pytest.mark.parametrize(
        'kwargs',
        [
            {'a': 0, 'b': 1, 'c': 1, 'alpha': 90, 'beta': 90, 'gamma': 90},
            {'a': -1, 'b': 1, 'c': 1, 'alpha': 90, 'beta': 90, 'gamma': 90},
            {'a': 1, 'b': 1, 'c': 1, 'alpha': 0, 'beta': 90, 'gamma': 90},
            {'a': 1, 'b': 1, 'c': 1, 'alpha': 180, 'beta': 90, 'gamma': 90},
        ],
    )
    def test_rejects_invalid_parameters(self, kwargs: dict):
        with pytest.raises(ValidationError):
            UnitCell(**kwargs)
