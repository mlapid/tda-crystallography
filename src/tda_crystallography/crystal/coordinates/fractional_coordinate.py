from typing import Self, Annotated

from pydantic.config import ConfigDict
from pydantic import BaseModel, Field, field_validator

class FractionalCoordinate(BaseModel):
    model_config = ConfigDict(
        title='FractionalCoordinate',
        frozen=False,
        arbitrary_types_allowed=False
    )

    x: Annotated[float, Field(ge=0, lt=1)]
    y: Annotated[float, Field(ge=0, lt=1)]
    z: Annotated[float, Field(ge=0, lt=1)]

    @field_validator('x', 'y', 'z', mode='before')
    @classmethod
    def wrap_to_unit(cls, value: float) -> float:
        return ((value % 1) + 1) % 1


    def __str__(self) -> str:
        return f"{self.__class__.__name__}(x={float(self.x)}, y={float(self.y)}, z={float(self.z)})"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x={float(self.x)}, y={float(self.y)}, z={float(self.z)})"
    
    def __eq__(self, coordinate: Self) -> bool:
        return (
            self.x == coordinate.x and \
            self.y == coordinate.y and \
            self.z == coordinate.z
        )