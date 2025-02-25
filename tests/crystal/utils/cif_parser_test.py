import pytest

from gemmi import cif

from tda_crystallography.crystal.utils.cif_parser import CifParser
from tda_crystallography.crystal.models.unit_cell import UnitCell
from tda_crystallography.crystal.models.symmetry import Symmetry
from tda_crystallography.crystal.models.fractional_coordinate import FractionalCoordinate

data_path: str = 'data/orthorhombic/AEI.cif'
doc: cif.Document = cif.read_file(data_path)
block: cif.Block = doc.sole_block()


class TestCifParser:

    @pytest.fixture
    def cif_parser(self) -> CifParser:
        return CifParser(block=block)
    
    def test_crystal_name(self, cif_parser: CifParser):
        assert cif_parser.crystal_name == 'AEI'
    
    def test_crystal_system(self, cif_parser: CifParser):
        assert cif_parser.crystal_system == 'Orthorhombic'

    def test_space_group(self, cif_parser: CifParser):
        assert cif_parser.space_group == 63

    def test_unit_cell(self, cif_parser: CifParser):
        expected_unit_cell: UnitCell = UnitCell(a=13.6770, b=12.6070, c=18.4970, alpha=90.0, beta=90.0, gamma=90.0)
        assert cif_parser.unit_cell == expected_unit_cell

    def test_symmetries(self, cif_parser: CifParser):
        expected_symmetries: set[Symmetry] = {
            Symmetry(operation='+x,+y,+z'),
            Symmetry(operation='1/2+x,1/2+y,+z'),
            Symmetry(operation='-x,+y,+z'),
            Symmetry(operation='1/2-x,1/2+y,+z'),
            Symmetry(operation='+x,-y,1/2+z'),
            Symmetry(operation='1/2+x,1/2-y,1/2+z'),
            Symmetry(operation='-x,-y,1/2+z'),
            Symmetry(operation='1/2-x,1/2-y,1/2+z'),
            Symmetry(operation='-x,-y,-z'),
            Symmetry(operation='1/2-x,1/2-y,-z'),
            Symmetry(operation='+x,-y,-z'),
            Symmetry(operation='1/2+x,1/2-y,-z'),
            Symmetry(operation='-x,+y,1/2-z'),
            Symmetry(operation='1/2-x,1/2+y,1/2-z'),
            Symmetry(operation='+x,+y,1/2-z'),
            Symmetry(operation='1/2+x,1/2+y,1/2-z')
        }
        assert cif_parser.symmetries == expected_symmetries

    def test_atomic_fractional_coordinates(self, cif_parser: CifParser):
        expected_atomic_fractional_coordinates: set[FractionalCoordinate] = {
            FractionalCoordinate(x=0.0000, y=0.0004, z=0.1614),
            FractionalCoordinate(x=0.1449, y=0.0438, z=0.2500),
            FractionalCoordinate(x=0.1252, y=0.1515, z=0.1293),
            FractionalCoordinate(x=0.1804, y=0.9517, z=0.1253),
            FractionalCoordinate(x=0.1465, y=0.8322, z=0.0116),
            FractionalCoordinate(x=0.0000, y=0.7364, z=0.9468),
            FractionalCoordinate(x=0.1794, y=0.6672, z=0.9281),
            FractionalCoordinate(x=0.7404, y=0.0000, z=0.0000),
            FractionalCoordinate(x=0.1126, y=0.0369, z=0.1664),
            FractionalCoordinate(x=0.1128, y=0.7711, z=0.9394),
            FractionalCoordinate(x=0.7733, y=0.9042, z=0.0521)
        }
        assert cif_parser.atomic_fractional_coordinates == expected_atomic_fractional_coordinates