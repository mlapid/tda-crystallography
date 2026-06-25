import pytest
import gemmi

from tda_crystallography.crystal.symmetry import Symmetry


class TestSymmetry:
    @pytest.mark.parametrize(
        'operation, expected_order',
        [
            ('+x,+y,+z', 1),
            ('X,Y,Z', 1),
            ('-x,-y,-z', 2),
            ('-x,-y,+z', 2),
            ('-y,x,z', 4),
            ('y,-x,z', 4),
            ('1/2+x,1/2+y,+z', 2),
            ('x,y,z+1/2', 2),
        ],
    )
    def test_order(self, operation: str, expected_order: int):
        symmetry = Symmetry(operation=operation)
        assert symmetry.order == expected_order

    def test_normalises_operation_triplet(self):
        symmetry = Symmetry(operation='+x,+y,+z')
        assert symmetry.operation.triplet() == 'x,y,z'

    def test_accepts_gemmi_op(self):
        operation = gemmi.Op('x,y,z')
        symmetry = Symmetry(operation=operation)
        assert symmetry.operation == operation
        assert symmetry.order == 1

    def test_equivalent_string_forms_are_equal(self):
        s1 = Symmetry(operation='+x,+y,+z')
        s2 = Symmetry(operation='x,y,z')
        assert s1 == s2

    def test_hashable_in_set(self):
        s1 = Symmetry(operation='+x,+y,+z')
        s2 = Symmetry(operation='x,y,z')
        assert {s1, s2} == {s1}

    def test_str_returns_triplet(self):
        symmetry = Symmetry(operation='1/2+x,1/2+y,+z')
        assert str(symmetry) == 'x+1/2,y+1/2,z'

    def test_repr_is_unambiguous(self):
        symmetry = Symmetry(operation='-y,x,z')
        assert repr(symmetry) == "Symmetry('-y,x,z')"

    def test_is_frozen(self):
        symmetry = Symmetry(operation='x,y,z')
        with pytest.raises(Exception):
            symmetry.operation = gemmi.Op('-x,-y,-z')