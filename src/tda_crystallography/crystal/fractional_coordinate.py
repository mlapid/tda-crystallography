from typing import Annotated

import numpy as np
from pydantic.config import ConfigDict
from pydantic import BaseModel, Field, field_validator

from tda_crystallography.crystal.unit_cell import UnitCell
from tda_crystallography.crystal.positional_coordinate import PositionalCoordinate


class FractionalCoordinate(BaseModel):
    model_config = ConfigDict(
        title='FractionalCoordinate',
        frozen=True,
        arbitrary_types_allowed=False
    )

    x: Annotated[float, Field(ge=0, lt=1)]
    y: Annotated[float, Field(ge=0, lt=1)]
    z: Annotated[float, Field(ge=0, lt=1)]

    @field_validator('x', 'y', 'z', mode='before')
    @classmethod
    def wrap_to_unit(cls, value: float) -> float:
        return ((value % 1) + 1) % 1
    
    def __hash__(self):
        return hash((self.__class__.__name__, self.x, self.y, self.z))

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}'
            f'(x={self.x:.5f}, y={self.y:.5f}, z={self.z:.5f})'
        )
    
    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}'
            f'(x={self.x}, y={self.y}, z={self.z})'
        )

    def orthogonalise(self, unit_cell: UnitCell) -> PositionalCoordinate:
        x, y, z = unit_cell.orthogonalisation_matrix @ np.array([self.x, self.y, self.z], dtype=float)
        return PositionalCoordinate(x=x, y=y, z=z)