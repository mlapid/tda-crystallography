import numpy as np
from pydantic import BaseModel
from pydantic.config import ConfigDict

from tda_crystallography.crystal.unit_cell import UnitCell
from tda_crystallography.crystal.symmetry import Symmetry
from tda_crystallography.crystal.fractional_coordinate import FractionalCoordinate
from tda_crystallography.crystal.positional_coordinate import PositionalCoordinate


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
    atomic_fractional_coordinates: set[FractionalCoordinate]

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'crystal_name={self.crystal_name!r}, '
            f'crystal_system={self.crystal_system!r}, '
            f'space_group={self.space_group}, '
            f'n_symmetries={len(self.symmetries)}, '
            f'n_atoms={len(self.atomic_fractional_coordinates)}'
            ')'
        )
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def extended_fractional_coordinates(self) -> set[FractionalCoordinate]:
        return {
            FractionalCoordinate(x=x, y=y, z=z)
            for symmetry in self.symmetries
            for coordinate in self.atomic_fractional_coordinates
            for x, y, z in [
                (symmetry.seitz_matrix @ np.array([coordinate.x, coordinate.y, coordinate.z, 1]))[:3]
            ]
        }
    
    def extended_positional_coordinates(self, *, normalise: bool = True) -> set[PositionalCoordinate]:
        coordinates: set[PositionalCoordinate] = {
            coordinate.orthogonalise(self.unit_cell)
            for coordinate in self.extended_fractional_coordinates
        }
        
        if not normalise:
            return coordinates

        k: float = self.unit_cell.normalising_constant

        return {coordinate.normalise(k) for coordinate in coordinates}