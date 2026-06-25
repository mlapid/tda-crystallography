from typing import Annotated
from math import cos, sin, sqrt, pi

import numpy as np
from pydantic.config import ConfigDict
from pydantic import BaseModel, Field


class UnitCell(BaseModel):
    model_config = ConfigDict(
        title='UnitCell',
        frozen=True,
        arbitrary_types_allowed=False
    )

    a: Annotated[float, Field(gt=0)]
    b: Annotated[float, Field(gt=0)]
    c: Annotated[float, Field(gt=0)]

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
        
        return np.linalg.det(self.orthogonalisation_matrix)

    @property
    def normalising_constant(self) -> float:
        return (1 / self.volume) ** (1/3)
    
    @property
    def orthogonalisation_matrix(self) -> np.ndarray:
        '''Convert fractional coordinates to positional coordinates.'''

        radians:   float = pi / 180
        
        alpha_rad: float = self.alpha * radians
        beta_rad:  float = self.beta * radians
        gamma_rad: float = self.gamma * radians

        sin_alpha: float = sin(alpha_rad)
        cos_alpha: float = cos(alpha_rad)
        cot_alpha: float = cos(alpha_rad) / sin(alpha_rad)
        csc_alpha: float = 1 / sin(alpha_rad)

        sin_beta: float = sin(beta_rad)
        cos_beta: float = cos(beta_rad)
        cot_beta: float = cos(beta_rad) / sin(beta_rad)
        csc_beta: float = 1 / sin(beta_rad)
        
        cos_gamma: float = cos(gamma_rad)

        a_x: float = self.a * sin_beta * sqrt(1 - (cot_alpha * cot_beta - csc_alpha * csc_beta * cos_gamma) ** 2)
        a_y: float = self.a * csc_alpha * cos_gamma - self.a * cot_alpha * cos_beta
        a_z: float = self.a * cos_beta

        return np.array([
            [a_x, 0, 0],
            [a_y, self.b * sin_alpha, 0],
            [a_z, self.b * cos_alpha, self.c],
        ])