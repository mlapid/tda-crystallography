import plotly.express as px
import numpy as np
import math

from typing import List
from fractions import Fraction
from random import random

from Symmetry import Symmetry
from UnitCell import UnitCell
from Fractional import FractionalCoordinate, FractionalCoordinateList
from Positional import PositionalCoordinate, PositionalCoordinateList

class RandomCrystal:

    def __init__(self, symmetries: List[Symmetry], n: int = 1):
        self.symmetries = symmetries
        self.n = n

        self.orbit_period: int = self.__generate_orbit_period()
        self.fractional_coordinates: FractionalCoordinateList = self.__generate(n)

    def __generate_random_fractional_coordinates(self, n: int) -> FractionalCoordinateList:
        
        fractionalCoordinates: FractionalCoordinateList = FractionalCoordinateList()
        
        for _ in range(n):

            x: Fraction = Fraction(random())
            y: Fraction = Fraction(random())
            z: Fraction = Fraction(random())

            fractionalCoordinates.append(FractionalCoordinate(x, y, z))
        
        return fractionalCoordinates
    
    def __generate_orbit_period(self) -> int:
        
        initial_coordinate: FractionalCoordinate = self.__generate_random_fractional_coordinates(1)[0]

        orbit: FractionalCoordinateList = FractionalCoordinateList()

        for symmetry in self.symmetries:
                initial_coordinate_orbit: FractionalCoordinate = symmetry.apply_to_fractional_coordinate(initial_coordinate)
                orbit.extend(initial_coordinate_orbit)

        return len(orbit)
    
    def __generate(self, n: int) -> FractionalCoordinateList:
        
        initial_coordinates: FractionalCoordinateList = self.__generate_random_fractional_coordinates(n)

        asymmetric_unit = FractionalCoordinateList()

        for symmetry in self.symmetries:
            for coordinate in initial_coordinates:
                extended_coordinate: FractionalCoordinate = symmetry.apply_to_fractional_coordinate(coordinate)
                asymmetric_unit.extend(extended_coordinate)

        return asymmetric_unit
    
    def apply_boundary_conditions(self, unit_cell: UnitCell) -> np.ndarray:

        if not unit_cell.is_normalised:
            unit_cell = unit_cell.normalise()

        positional_coordinates = self.fractional_coordinates.orthogonalise(unit_cell)

        n = len(positional_coordinates)
        distance_matrix: np.array = np.zeros((n, n))

        for i in range(n):
            coordinate_one: PositionalCoordinate = positional_coordinates[i]
            for j in range(i+1, n):
                coordinate_two: PositionalCoordinate = positional_coordinates[j]

                dist_x: float; dist_y: float; dist_z: float
                dist_x, dist_y, dist_z = coordinate_one[i].distance(coordinate_two[j])

                if dist_x > unit_cell.a:
                    dist_x = 1 - dist_x
                if dist_y > unit_cell.b:
                    dist_y = 1 - dist_y
                if dist_z > unit_cell.c:
                    dist_z = 1 - dist_z
                if boundary_conditions:
                    dist_x, dist_y, dist_z = self.__apply_boundary_conditions(dist_x, dist_y, dist_z)
                distance: float = math.sqrt(dist_x ** 2 + dist_y ** 2 + dist_z ** 2)
                distance_matrix[i][j] = distance
                distance_matrix[j][i] = distance

        return distance_matrix
    
    def plot(self) -> None:
        # Plot in 3D Cartesian coordinates

        data_frame = self.fractional_coordinates.to_dataframe()

        fig = px.scatter_3d(
            data_frame, x='x', y='y', z='z'
        )
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        fig.show()