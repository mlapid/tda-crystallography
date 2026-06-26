import numpy as np
from pydantic import BaseModel
from pydantic.config import ConfigDict

from tda_crystallography.crystal.atom import Atom
from tda_crystallography.crystal.positional_atom import PositionalAtom
from tda_crystallography.crystal.unit_cell import UnitCell
from tda_crystallography.crystal.symmetry import Symmetry
from tda_crystallography.crystal.fractional_coordinate import FractionalCoordinate


class Crystal(BaseModel):
    model_config = ConfigDict(
        title='Crystal',
        frozen=True,
        arbitrary_types_allowed=True
    )

    crystal_name: str
    crystal_system: str
    space_group: int

    unit_cell: UnitCell
    symmetries: set[Symmetry]
    atom_sites: list[Atom]

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'crystal_name={self.crystal_name!r}, '
            f'crystal_system={self.crystal_system!r}, '
            f'space_group={self.space_group}, '
            f'n_symmetries={len(self.symmetries)}, '
            f'n_atom_sites={len(self.atom_sites)}'
            ')'
        )
    
    def __repr__(self) -> str:
        return self.__str__()

    @property
    def unit_cell_atoms(self) -> set[Atom]:
        return {
            Atom(
                label=atom_site.label,
                element=atom_site.element,
                fractional_coordinate=FractionalCoordinate(
                    x=x,
                    y=y,
                    z=z,
                ),
            )
            for symmetry in self.symmetries
            for atom_site in self.atom_sites
            for x, y, z in [
                (symmetry.seitz_matrix @ np.array([atom_site.fractional_coordinate.x, atom_site.fractional_coordinate.y, atom_site.fractional_coordinate.z, 1]))[:3]
            ]
        }

    def unit_cell_positional_atoms(self, *, normalise: bool = False) -> set[PositionalAtom]:
        return {
            atom.to_positional_atom(self.unit_cell, normalise=normalise)
            for atom in self.unit_cell_atoms
        }