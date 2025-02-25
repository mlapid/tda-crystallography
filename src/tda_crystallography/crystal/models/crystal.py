from typing import Literal
from fractions import Fraction

import numpy as np
import pandas as pd
import plotly.express as px
from pydantic import BaseModel

from tda_crystallography.crystal.models.unit_cell import UnitCell
from tda_crystallography.crystal.models.symmetry import Symmetry
from tda_crystallography.crystal.models.fractional_coordinate import FractionalCoordinate
from tda_crystallography.crystal.models.positional_coordinate import PositionalCoordinate

class Crystal(BaseModel):
    crystal_name: str
    crystal_system: str
    space_group: int
    unit_cell: UnitCell
    symmetries: set[Symmetry]
    atomic_fractional_coordinates: set[FractionalCoordinate]

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'crystal_name={self.crystal_name}, '
            f'crystal_system={self.crystal_system}, '
            f'space_group={self.space_group}, '
            f'unit_cell={self.unit_cell}'
            # f'symmetries={self.symmetries}, '
            # f'atomic_fractional_coordinates={self.atomic_fractional_coordinates}'
            ')'
        )
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def extended_fractional_coordinates(self) -> set[FractionalCoordinate]:
        extended_fractional_coordinates: set[FractionalCoordinate] = set()

        for symmetry in self.symmetries:
            seitz_matrix: np.ndarray = np.array(symmetry.operation.seitz())
            for coordinate in self.atomic_fractional_coordinates:
                x, y, z = coordinate.x, coordinate.y, coordinate.z
                transformed_coordinate: np.ndarray = seitz_matrix @ np.array([x, y, z, Fraction(1)])
                x_prime, y_prime, z_prime, _ = transformed_coordinate
                extended_fractional_coordinates.add(FractionalCoordinate(x=x_prime, y=y_prime, z=z_prime))

        return extended_fractional_coordinates
    
    @property
    def extended_positional_coordinates(self) -> set[PositionalCoordinate]:
        return {coordinate.orthogonalise(self.unit_cell) for coordinate in self.extended_fractional_coordinates}
    
    @property
    def df_fractional_coordinates(self) -> pd.DataFrame:
        return self._create_dataframe(self.extended_fractional_coordinates)

    @property
    def df_positional_coordinates(self) -> pd.DataFrame:
        return self._create_dataframe(self.extended_positional_coordinates)
    
    def _create_dataframe(self, coordinates: set[FractionalCoordinate | PositionalCoordinate]) -> pd.DataFrame:
        data: list[tuple[float, float, float]] = [(float(c.x), float(c.y), float(c.z)) for c in coordinates]
        df: pd.DataFrame = pd.DataFrame(data=data, columns=['x', 'y', 'z'])
        df = df.sort_values(by=['x', 'y', 'z'], ignore_index=True)
        return df

    def plot(self, coordinate_type: Literal['fractional', 'positional'] = 'positional') -> None:
        if coordinate_type == 'fractional':
            df: pd.DataFrame = self.df_fractional_coordinates
        elif coordinate_type == 'positional':
            df: pd.DataFrame = self.df_positional_coordinates
        
        fig = px.scatter_3d(
            df, x='x', y='y', z='z',
            size_max = 6,
            title=f'3D Scatter Plot of {self.crystal_name} crystal ({coordinate_type} coordinates)',
            labels={'x': 'X Coordinate', 'y': 'Y Coordinate', 'z': 'Z Coordinate'}
        )
        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),
            scene=dict(
                xaxis_title='X Axis',
                yaxis_title='Y Axis',
                zaxis_title='Z Axis'
            )
        )
        fig.show()