import plotly.express as px
import numpy as np

from typing import List
from fractions import Fraction
from random import random

from Symmetry import Symmetry
from Fractional import FractionalCoordinate, FractionalCoordinateList

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
    
    def apply_boundary_conditions(self) -> np.ndarray:

        distance_matrix: np.ndarray = self.fractional_coordinates.calculate_distance_matrix(boundary_conditions=True)

        return distance_matrix
    
    def plot(self) -> None:
        # Plot in 3D Cartesian coordinates

        data_frame = self.fractional_coordinates.to_dataframe()

        fig = px.scatter_3d(
            data_frame, x='x', y='y', z='z'
        )
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        fig.show()