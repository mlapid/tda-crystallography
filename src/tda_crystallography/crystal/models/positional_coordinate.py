from __future__ import annotations

from typing import Self

from pydantic.config import ConfigDict
from pydantic import BaseModel

class PositionalCoordinate(BaseModel):
    model_config = ConfigDict(
        title='PositionalCoordinate',
        frozen=True,
        arbitrary_types_allowed=False
    )

    x: float
    y: float
    z: float

    def __hash__(self):
        return hash((self.__class__.__name__, self.x, self.y, self.z))

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, z={self.z})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def normalise(self, normalising_constant: float) -> PositionalCoordinate:
        x = self.x * normalising_constant
        y = self.y * normalising_constant
        z = self.z * normalising_constant

        return PositionalCoordinate(x=x, y=y, z=z)
    
    