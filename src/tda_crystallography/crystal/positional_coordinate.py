from typing import Self

from pydantic import BaseModel
from pydantic.config import ConfigDict


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
        return (
            f'{self.__class__.__name__}('
            f'x={self.x}, '
            f'y={self.y}, '
            f'z={self.z}'
            ')'
        )
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def normalise(self, normalising_constant: float) -> Self:
        if normalising_constant <= 0:
            raise ValueError('Normalising constant must be positive.')

        x: float = self.x * normalising_constant
        y: float = self.y * normalising_constant
        z: float = self.z * normalising_constant

        return self.model_copy(update={'x': x, 'y': y, 'z': z})