from fractions import Fraction
from typing import Annotated

from pydantic.config import ConfigDict
from pydantic import BaseModel, Field, field_validator

from tda_crystallography.crystal.models.unit_cell import UnitCell
from tda_crystallography.crystal.models.positional_coordinate import PositionalCoordinate

class FractionalCoordinate(BaseModel):
    model_config = ConfigDict(
        title='FractionalCoordinate',
        frozen=False,
        arbitrary_types_allowed=False
    )

    x: Annotated[Fraction, Field(ge=0, lt=1)]
    y: Annotated[Fraction, Field(ge=0, lt=1)]
    z: Annotated[Fraction, Field(ge=0, lt=1)]

    @field_validator('x', 'y', 'z', mode='before')
    @classmethod
    def wrap_to_unit(cls, value: Fraction) -> Fraction:
        return ((value % 1) + 1) % 1

    @field_validator('x', 'y', 'z', mode='before')
    @classmethod
    def convert_to_fraction(cls, value: float) -> Fraction:
        return Fraction(value)
    
    def __hash__(self):
        return hash((self.__class__.__name__, self.x, self.y, self.z))

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(x={float(self.x)}, y={float(self.y)}, z={float(self.z)})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def orthogonalise(self, unit_cell: UnitCell) -> PositionalCoordinate:
        x, y, z = unit_cell.orthogonalisation_matrix @ [self.x, self.y, self.z]
        return PositionalCoordinate(x=x, y=y, z=z)