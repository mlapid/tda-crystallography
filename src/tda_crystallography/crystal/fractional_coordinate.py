from typing import Annotated

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
        return f'{self.__class__.__name__}(x={self.x}, y={self.y}, z={self.z})'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def orthogonalise(self, unit_cell: UnitCell) -> PositionalCoordinate:
        x, y, z = unit_cell.orthogonalisation_matrix @ [self.x, self.y, self.z]
        return PositionalCoordinate(x=float(x), y=float(y), z=float(z))