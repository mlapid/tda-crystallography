import pytest

from tda_crystallography.crystal.models.symmetry import Symmetry

class TestSymmetry:

    @pytest.fixture
    def symmetry(self) -> Symmetry:
        return Symmetry(operation='x+1/2,y+1/2,z')
    
    def test_order(self, symmetry: Symmetry):
        assert symmetry.order == 2
        
        