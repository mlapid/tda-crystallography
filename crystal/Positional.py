from __future__ import annotations

import gemmi
from typing import Self, List, Dict, Self
from itertools import combinations
import math
import numpy as np
import pandas as pd
from collections import UserList
from UnitCell import UnitCell

class PositionalCoordinate:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

        self.is_normalised: bool = False

    def __eq__(self, coordinate: PositionalCoordinate) -> bool:
        if (self.x == coordinate.x and \
             self.y == coordinate.y and \
            self.z == coordinate.z):
            return True
        else:
            return False
        
    def __hash__(self):
        return hash((self.__class__.__name__, self.x, self.y, self.z))
        
    def __str__(self) -> str:

        x = round(self.x, 4)
        y = round(self.y, 4)
        z = round(self.z, 4)

        return f'{self.__class__.__name__}({x}, {y}, {z})'
    
    def __repr__(self) -> str:

        x = round(self.x, 4)
        y = round(self.y, 4)
        z = round(self.z, 4)

        return f'{self.__class__.__name__}({x}, {y}, {z})'
    
    def normalise(self, normalising_constant: float) -> Self:

        if self.is_normalised:
            raise AssertionError(f"Positional coordinate {self} is already normalised.")

        self.x *= normalising_constant
        self.y *= normalising_constant
        self.z *= normalising_constant

        self.is_normalised = True

        return self
    
    def distance(self, positionalCoordinate: PositionalCoordinate) -> float:

        dist_x: float = abs(self.x - positionalCoordinate.x)
        dist_y: float = abs(self.y - positionalCoordinate.y)
        dist_z: float = abs(self.z - positionalCoordinate.z)

        return [dist_x, dist_y, dist_z]



class PositionalCoordinateList(UserList):

    def __init__(self):
        super().__init__()

        self.is_normalised: bool = False

    def __contains__(self, coordinate: PositionalCoordinate) -> bool:

        for item in self:
            if coordinate == item:
                return True
        return False

    def append(self, coordinate: PositionalCoordinate) -> None:
        if not isinstance(coordinate, PositionalCoordinate):
            raise TypeError("PositionalCoordinateList can only append Positional coordinates")
        if coordinate not in self:
            super().append(coordinate)
        else:
            return
        
    def normalise(self, normalising_constant: float) -> Self:

        if self.is_normalised:
            raise AssertionError(f"{self.__class__.__name__} {id(self)} is already normalised.")

        for positional_coordinate in self:
            positional_coordinate.normalise(normalising_constant)

        self.is_normalised = True

        return self
    
    def calculate_distance(self) -> Dict[tuple: float]:

        distance_dict: Dict[tuple, float] = {}
        coordinate_pairs = list(combinations(self, 2))

        for pair in coordinate_pairs:
            distance: float = pair[0].distance(pair[1])
            distance_dict[pair] = distance

        # Sort the dictionary by distance
        distance_dict = dict(sorted(distance_dict.items(), key=lambda item: item[1], reverse=False))

        return distance_dict
    
    # def calculate_distance_matrix(self) -> np.array:

    #     n = len(self)
    #     distance_matrix: np.array = np.zeros((n, n))

    #     for i in range(n):
    #         coordinate_one: PositionalCoordinate = self[i]
    #         for j in range(n):
    #             if i == j:
    #                 distance_matrix[i][j] = 0
    #                 continue
                
    #             coordinate_two = self[j]

    #             dist_x, dist_y, dist_z = coordinate_one.distance(coordinate_two)
    #             distance: float = math.sqrt(dist_x ** 2 + dist_y ** 2 + dist_z ** 2)
    #             distance_matrix[i][j] = distance

    #     return distance_matrix
    
    def calculate_distance_matrix(self, unit_cell, boundary_conditions: bool) -> np.array:

        n = len(self)
        distance_matrix: np.array = np.zeros((n, n))

        for i in range(n):
            for j in range(i+1, n):
                dist_x: float; dist_y: float; dist_z: float
                dist_x, dist_y, dist_z = self[i].distance(self[j])
                if boundary_conditions:
                    if dist_x > 1/2 * unit_cell.a:
                        dist_x = unit_cell.a - dist_x
                    if dist_y > 1/2 * unit_cell.b:
                        dist_y = unit_cell.b - dist_y
                    if dist_z > 1/2 * unit_cell.c:
                        dist_z = unit_cell.c - dist_z
                distance: float = math.sqrt(dist_x ** 2 + dist_y ** 2 + dist_z ** 2)
                distance_matrix[i][j] = distance
                distance_matrix[j][i] = distance

        return distance_matrix
    
    def to_dataframe(self) -> pd.DataFrame:

        data = list(map(
            lambda coordinate: [coordinate.x, coordinate.y, coordinate.z],
            self
        ))

        data_frame = pd.DataFrame(data, columns=['x', 'y', 'z'])

        return data_frame