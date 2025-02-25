import re
from fractions import Fraction

from gemmi import cif

from tda_crystallography.crystal.models.unit_cell import UnitCell
from tda_crystallography.crystal.models.symmetry import Symmetry
from tda_crystallography.crystal.models.fractional_coordinate import FractionalCoordinate

class CifParser:
    def __init__(self, block: cif.Block):
        self.block = block

    @property
    def crystal_name(self) -> str:
        '''The name of the crystal from the CIF block.'''
        return self.block.name
    
    @property
    def crystal_system(self) -> str:
        return self.block.find_value('_symmetry_cell_setting').capitalize()
    
    @property
    def space_group(self) -> int:
        return int(self.block.find_value('_symmetry_Int_Tables_number'))
    
    @property
    def unit_cell(self) -> UnitCell:
        '''The unit cell of the crystal from the CIF block.'''

        # Match for floating point number
        regex = r"[+-]?([0-9]*[.])?[0-9]+"

        a = float(re.search(regex, self.block.find_value('_cell_length_a')).group())
        b = float(re.search(regex, self.block.find_value('_cell_length_b')).group())
        c = float(re.search(regex, self.block.find_value('_cell_length_c')).group())

        alpha = float(re.search(regex, self.block.find_value('_cell_angle_alpha')).group())
        beta =  float(re.search(regex, self.block.find_value('_cell_angle_beta')).group())
        gamma = float(re.search(regex, self.block.find_value('_cell_angle_gamma')).group())
        
        return UnitCell(a=a, b=b, c=c, alpha=alpha, beta=beta, gamma=gamma)
    
    @property
    def symmetries(self) -> set[Symmetry]:
        return {Symmetry(operation=s.strip('"\'')) for s in self.block.find_values('_symmetry_equiv_pos_as_xyz')}
    
    @property
    def atomic_fractional_coordinates(self) -> set[FractionalCoordinate]:
        x: list[float] = [float(x) for x in self.block.find_values('_atom_site_fract_x')]
        y: list[float] = [float(y) for y in self.block.find_values('_atom_site_fract_y')]
        z: list[float] = [float(z) for z in self.block.find_values('_atom_site_fract_z')]

        return {FractionalCoordinate(x=x, y=y, z=z) for x, y, z in zip(x, y, z)}