import re
import abc
import gemmi

from gemmi import cif
from fractions import Fraction
from typing import List, Dict

from UnitCell import UnitCell
from Fractional import FractionalCoordinate, FractionalCoordinateList
from Symmetry import Symmetry

class BlockInterface(metaclass = abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load_data_source') and 
                callable(subclass.load_data_source) and 
                hasattr(subclass, 'extract_text') and 
                callable(subclass.extract_text) or 
                NotImplemented)
    
    @abc.abstractmethod
    def get_crystal_name(self) -> str:
        '''Get crystal name'''
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_unit_cell(self) -> UnitCell:
        '''Get unit cell'''
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_space_group_number(self) -> int:
        '''Get space group number'''
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_crystal_system(self) -> str:
        '''Get crystal system'''
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_symmetries(self) -> List[Symmetry]:
        '''Get symmetries'''
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_asymmetric_unit(self) -> FractionalCoordinateList:
        '''Get initial fractional coordinates'''
        raise NotImplementedError

class BlockSolo(BlockInterface):

    def __init__(self, block: cif.Block):
        self.block: cif.Block = block

    def get_crystal_name(self) -> str:
        return self.block.name

    def get_unit_cell(self) -> UnitCell:

        # Match for floating point number
        regex = r"[+-]?([0-9]*[.])?[0-9]+"

        a = float(re.search(regex, self.block.find_value('_cell_length_a')).group())
        b = float(re.search(regex, self.block.find_value('_cell_length_b')).group())
        c = float(re.search(regex, self.block.find_value('_cell_length_c')).group())

        alpha = float(re.search(regex, self.block.find_value('_cell_angle_alpha')).group())
        beta = float(re.search(regex, self.block.find_value('_cell_angle_beta')).group())
        gamma = float(re.search(regex, self.block.find_value('_cell_angle_gamma')).group())

        return UnitCell(a, b, c, alpha, beta, gamma)
    
    def get_space_group_number(self) -> int:
        return int(self.block.find_value('_symmetry_Int_Tables_number'))
    
    def get_crystal_system(self) -> str:
        return self.block.find_value('_symmetry_cell_setting').capitalize()

    def get_symmetries(self) -> List[Symmetry]:

        symmetries: List[Symmetry] = [Symmetry(s.strip('"\'')) for s in self.block.find_values('_symmetry_equiv_pos_as_xyz')]

        return symmetries
    
    # def get_initial_atoms(self) -> Dict[FractionalCoordinate, str]:

    #     atoms: List[str] = [str(atom) for atom in self.block.find_values('_atom_site_type_symbol')]

    #     initialFractionalCoordinates: FractionalCoordinateList = self.get_initial_fractional_coordinates()

    #     return dict(zip(initialFractionalCoordinates, atoms))
    
    def get_asymmetric_unit(self) -> FractionalCoordinateList:

        fractionalCoordinateList: FractionalCoordinateList = FractionalCoordinateList()

        x: List[Fraction] = [Fraction(x) for x in self.block.find_values('_atom_site_fract_x')]
        y: List[Fraction] = [Fraction(y) for y in self.block.find_values('_atom_site_fract_y')]
        z: List[Fraction] = [Fraction(z) for z in self.block.find_values('_atom_site_fract_z')]

        for index, element in enumerate(list(zip(x, y, z))):
            fractionalCoordinate: FractionalCoordinate = FractionalCoordinate(element[0], element[1], element[2])
            fractionalCoordinateList.append(fractionalCoordinate)

        return fractionalCoordinateList
    
class BlockTopos(BlockInterface):
    
    def __init__(self, block: cif.Block):
        self.block = block

    def get_crystal_name(self) -> str:
        return self.block.find_value('_chemical_formula_structural')

    def get_unit_cell(self) -> UnitCell:

        # Match for floating point number
        regex = r"[+-]?([0-9]*[.])?[0-9]+"

        a = float(re.search(regex, self.block.find_value('_cell_length_a')).group())
        b = float(re.search(regex, self.block.find_value('_cell_length_b')).group())
        c = float(re.search(regex, self.block.find_value('_cell_length_c')).group())

        alpha = float(re.search(regex, self.block.find_value('_cell_angle_alpha')).group())
        beta = float(re.search(regex, self.block.find_value('_cell_angle_beta')).group())
        gamma = float(re.search(regex, self.block.find_value('_cell_angle_gamma')).group())

        return UnitCell(a, b, c, alpha, beta, gamma)
    
    def get_space_group_number(self) -> int:

        space_group: int = int(self.block.find_value('_symmetry_int_tables_number'))

        return space_group
    
    def get_crystal_system(self) -> str:

        space_group: int = self.get_space_group_number()
        
        if 1 <= space_group <= 2:
            return "Triclinic"
        elif 3 <= space_group <= 15:
            return "Monoclinic"
        elif 16 <= space_group <= 74:
            return "Orthorhombic"
        elif 75 <= space_group <= 142:
            return "Tetragonal"
        elif 143 <= space_group <= 167:
            return "Trigonal"
        elif 168 <= space_group <= 194:
            return "Hexagonal"
        elif 195 <= space_group <= 230:
            return "Cubic"
        else:
            print("Invalid space group number")
            raise ValueError
    
    def get_symmetries(self) -> List[Symmetry]:

        symmetries: List[Symmetry] = [Symmetry(s.strip('"\'')) for s in self.block.find_values('_space_group_symop_operation_xyz')]

        return symmetries
    
    def get_asymmetric_unit(self) -> FractionalCoordinateList:

        fractionalCoordinateList: FractionalCoordinateList = FractionalCoordinateList()

        x: List[Fraction] = [Fraction(x) for x in self.block.find_values('_atom_site_fract_x')]
        y: List[Fraction] = [Fraction(y) for y in self.block.find_values('_atom_site_fract_y')]
        z: List[Fraction] = [Fraction(z) for z in self.block.find_values('_atom_site_fract_z')]

        for index, element in enumerate(list(zip(x, y, z))):
            fractionalCoordinate: FractionalCoordinate = FractionalCoordinate(element[0], element[1], element[2])
            fractionalCoordinateList.append(fractionalCoordinate)

        return fractionalCoordinateList