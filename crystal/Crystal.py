import plotly.express as px
import os
import gemmi
from gemmi import cif
import pandas as pd
import numpy as np
from typing import List
#from Block import Block
from UnitCell import UnitCell
from Symmetry import Symmetry
from Fractional import FractionalCoordinate, FractionalCoordinateList
from Positional import PositionalCoordinateList
import math
from utils import generate_random_fractional_coordinates


class Crystal:

    def __init__(self, block, apply_boundary_conditions=False, normalise=False):
        self.block = block

        self.name: str = self.block.get_crystal_name()
        self.unit_cell: UnitCell = self.block.get_unit_cell()
        self.space_group: int = self.block.get_space_group_number()
        self.system: str = self.block.get_crystal_system()
        self.symmetries: List[Symmetry] = self.block.get_symmetries()
        self.asymmetric_unit: FractionalCoordinateList = self.block.get_asymmetric_unit()

        self.random_asymmetric_unit: int = self.generate_random_asymmetric_unit()

        self.fractional_coordinates: FractionalCoordinateList = self.get_fractional_coordinates()
        self.positional_coordinates: PositionalCoordinateList = self.get_positional_coordinates(self.fractional_coordinates)

        if normalise:
            self.positional_coordinates.normalise(self.unit_cell.normalising_constant())

        self.data_frame: pd.DataFrame = self.positional_coordinates.to_dataframe()
        # self.distance_matrix: np.array = self.calculate_distance_matrix(self.fractional_coordinates, apply_boundary_conditions)

    def __str__(self) -> str:
        return f'Crystal of {len(self.positional_coordinates)} vertices with a unit cell {self.unit_cell}'
    
    def generate_random_asymmetric_unit(self) -> FractionalCoordinateList:
        
        single_fractional_coordinate: FractionalCoordinate = generate_random_fractional_coordinates(1)[0]

        extendedFractionalCoordinateList: FractionalCoordinateList = FractionalCoordinateList()

        for symmetry in self.symmetries:
                extendedFractionalCoordinate: FractionalCoordinate = symmetry.apply_to_fractional_coordinate(single_fractional_coordinate)
                extendedFractionalCoordinateList.extend(extendedFractionalCoordinate)

        return extendedFractionalCoordinateList
    
    def get_fractional_coordinates(self) -> FractionalCoordinateList:

        initial_fractional_coordinates: FractionalCoordinateList = self.asymmetric_unit

        # max_value = 576
        # n: int = len(self.random_asymmetric_unit)
        # assert(max_value % n == 0)
        # n = max_value // n
        # initial_fractional_coordinates: FractionalCoordinateList = generate_random_fractional_coordinates(n)

        extendedFractionalCoordinateList = FractionalCoordinateList()

        for symmetry in self.symmetries:
            for coordinate in initial_fractional_coordinates:
                extendedFractionalCoordinateList.extend(symmetry.apply_to_fractional_coordinate(coordinate))

        return extendedFractionalCoordinateList
    
    def get_positional_coordinates(self, fractionalCoordinateList: FractionalCoordinateList) -> PositionalCoordinateList:

        return fractionalCoordinateList.orthogonalise(self.unit_cell)

    def plot(self) -> None:
        # Plot in 3D Cartesian coordinates

        fig = px.scatter_3d(
            self.data_frame, x='x', y='y', z='z',
            size_max = 6,
        )
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        fig.show()