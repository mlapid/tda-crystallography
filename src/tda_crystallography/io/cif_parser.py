from pathlib import Path
from typing import Self

from gemmi import cif

from tda_crystallography.crystal.atom import Atom
from tda_crystallography.crystal.crystal import Crystal
from tda_crystallography.crystal.symmetry import Symmetry
from tda_crystallography.crystal.unit_cell import UnitCell
from tda_crystallography.crystal.fractional_coordinate import FractionalCoordinate


class CifParser:
    def __init__(self, block: cif.Block):
        self.block = block

    def parse(self) -> Crystal:
        return Crystal(
            crystal_name=self.crystal_name,
            crystal_system=self.crystal_system,
            space_group=self.space_group,
            unit_cell=self.unit_cell,
            symmetries=self.symmetries,
            atom_sites=self.atom_sites,
        )

    @classmethod
    def from_file(cls, path: str | Path, *, block_name: str | None = None) -> Self:
        doc: cif.Document = cif.read_file(str(path))
        block: cif.Block = doc[block_name] if block_name else doc.sole_block()

        return cls(block=block)

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

        a: float = cif.as_number(self.block.find_value('_cell_length_a'))
        b: float = cif.as_number(self.block.find_value('_cell_length_b'))
        c: float = cif.as_number(self.block.find_value('_cell_length_c'))

        alpha: float = cif.as_number(self.block.find_value('_cell_angle_alpha'))
        beta:  float = cif.as_number(self.block.find_value('_cell_angle_beta'))
        gamma: float = cif.as_number(self.block.find_value('_cell_angle_gamma'))
        
        return UnitCell(a=a, b=b, c=c, alpha=alpha, beta=beta, gamma=gamma)
    
    @property
    def symmetries(self) -> set[Symmetry]:
        return {Symmetry(operation=s.strip('"\'')) for s in self.block.find_values('_symmetry_equiv_pos_as_xyz')}
    
    @property
    def atom_sites(self) -> list[Atom]:
        return [
            Atom(
                label=label,
                element=element,
                fractional_coordinate=FractionalCoordinate(
                    x=cif.as_number(x),
                    y=cif.as_number(y),
                    z=cif.as_number(z),
                )
            )
            for label, element, x, y, z in zip(
                self.block.find_values('_atom_site_label'),
                self.block.find_values('_atom_site_type_symbol'),
                self.block.find_values('_atom_site_fract_x'),
                self.block.find_values('_atom_site_fract_y'),
                self.block.find_values('_atom_site_fract_z'),
            )
        ]