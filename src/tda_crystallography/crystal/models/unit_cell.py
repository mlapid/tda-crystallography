from typing import Annotated
from math import cos, sqrt, pi

import numpy as np
from pydantic import BaseModel, Field

class UnitCell(BaseModel):
    a: Annotated[float, Field(ge=0)]
    b: Annotated[float, Field(ge=0)]
    c: Annotated[float, Field(ge=0)]

    alpha: Annotated[float, Field(gt=0, lt=180)]
    beta:  Annotated[float, Field(gt=0, lt=180)]
    gamma: Annotated[float, Field(gt=0, lt=180)]

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'a={self.a}, '
            f'b={self.b}, '
            f'c={self.c}, '
            f'alpha={self.alpha}, '
            f'beta={self.beta}, '
            f'gamma={self.gamma}'
            ')'
        )
    
    def __repr__(self) -> str:
        return self.__str__()

    @property
    def volume(self) -> float:
        radians:   float = pi / 180
        alpha_rad: float = self.alpha * radians
        beta_rad:  float = self.beta * radians
        gamma_rad: float = self.gamma * radians

        volume: float = self.a * self.b * self.c * \
            sqrt(1 + 2 * cos(alpha_rad) * cos(beta_rad) * cos(gamma_rad) - \
                cos(alpha_rad)**2 - cos(beta_rad)**2 - cos(gamma_rad)**2
            )

        return volume

    @property
    def normalising_constant(self) -> float:
        return (1 / self.volume) ** (1/3)
    
    @property
    def orthogonalisation_matrix(self) -> np.ndarray:

        return np.array([
            [self.a, 0, 0],
            [0, self.b, 0],
            [0, 0, self.c]
        ])
    