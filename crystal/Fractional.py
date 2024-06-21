from __future__ import annotations

import gemmi
import math
import numpy as np
import pandas as pd
from collections import UserList
from typing import List, Dict, Tuple, Self, override
from itertools import combinations
from fractions import Fraction

from UnitCell import UnitCell
from Positional import PositionalCoordinate, PositionalCoordinateList
# from Symmetry import Symmetry


class FractionalCoordinate:

    ROUND_OFF: int = 4

    def __init__(self, x: Fraction, y: Fraction, z: Fraction):
        if not isinstance(x, Fraction) or not isinstance(y, Fraction) or not isinstance(z, Fraction):
            raise TypeError(f"FractionalCoordinate should be initialised with Fractions, got {x, y, z} instead.")
        if not (0 <= x <= 1 and 0 <= y <= 1 and 0 <= z <= 1):
            x, y, z = self.__wrap_to_unit(x, y, z)
            self.x = x
            self.y = y
            self.z = z
        else:
            self.x = x
            self.y = y
            self.z = z

    @classmethod
    def __wrap_to_unit(cls, x, y, z) -> Tuple[Fraction, Fraction, Fraction]:

        x = ((x % 1) + 1) % 1
        y = ((y % 1) + 1) % 1
        z = ((z % 1) + 1) % 1

        return x, y, z

    def __eq__(self, other: FractionalCoordinate) -> bool:
        if (self.x == other.x and \
             self.y == other.y and \
            self.z == other.z):
            return True
        else:
            return False
        
        # if self.distance(other) < 1e-3:
        #     return True
        # else:
        #     return False
        
    def __hash__(self):
        return hash((self.__class__.__name__, self.x, self.y, self.z))
        
    def __str__(self) -> str:

        return f'{self.__class__.__name__}({float(self.x)}, {float(self.y)}, {float(self.z)})'
        #return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z})'
    
    def __repr__(self) -> str:

        return f'{self.__class__.__name__}({float(self.x)}, {float(self.y)}, {float(self.z)})'
        #return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z})'
    
    def to_vector(self) -> np.array:

        return np.array([self.x, self.y, self.z])
    
    def orthogonalise(self, unitCell: UnitCell) -> PositionalCoordinate:

        positionalCoordinate: gemmi.Position = unitCell.orthogonalize(self)

        return PositionalCoordinate(positionalCoordinate.x, positionalCoordinate.y, positionalCoordinate.z)
    
    def distance(self, fractionalCoordinate: FractionalCoordinate) -> List[float]:

        dist_x: float = float(self.x - fractionalCoordinate.x)
        dist_y: float = float(self.y - fractionalCoordinate.y)
        dist_z: float = float(self.z - fractionalCoordinate.z)

        return [dist_x, dist_y, dist_z]
    

class FractionalCoordinateList(UserList):

    def __contains__(self, other: FractionalCoordinate) -> bool:

        for item in self:
            if other == item:
                return True
        return False

    @override
    def append(self, coordinate: FractionalCoordinate) -> None:
        if not isinstance(coordinate, FractionalCoordinate):
            raise TypeError(f"FractionalList can only append Fractional coordinates, got {coordinate} instead.")
        if coordinate not in self:
            super().append(coordinate)
        else:
            # print(f"Coordinate {coordinate} already exists in the list.")
            return
    
    @override
    def extend(self, coordinateList: FractionalCoordinateList) -> None:
        if not isinstance(coordinateList, FractionalCoordinateList):
            raise TypeError(f"FractionalList can only extend Fractional coordinate lists, got {coordinateList} instead.")
        
        for coordinate in coordinateList:
            if coordinate not in self:
                # Coordinate does not exist in the list
                super().append(coordinate)
                continue
            else:
                # print(f"Coordinate {coordinate} already exists in the list.")
                continue
        
    # def apply_symmetries(self, symmetries: List[Symmetry]) -> FractionalCoordinateList:

    #     if not isinstance(symmetries, list):
    #         symmetries = [symmetries]

    #     updatedFractionalCoordinateList = FractionalCoordinateList()
        
    #     for symmetry in symmetries:
    #         for coordinate in self:
    #             transformedCoordinateList: FractionalCoordinateList = coordinate.apply_symmetry(symmetry)
    #             updatedFractionalCoordinateList.extend(transformedCoordinateList)
        
    #     return updatedFractionalCoordinateList
    
    def orthogonalise(self, unit_cell: UnitCell) -> PositionalCoordinateList:

        positionalCoordinateList: PositionalCoordinateList = PositionalCoordinateList()

        coordinate_list: List[Tuple] = list(zip(*(np.array(unit_cell.orth.mat) @ self.to_array().T)))

        for coordinate in coordinate_list:
            x, y, z = coordinate
            positionalCoordinateList.append(PositionalCoordinate(x, y, z))

        return positionalCoordinateList
    
    def calculate_distance(self) -> Dict[tuple: float]:

        distance_dict: Dict[tuple, float] = {}
        coordinate_pairs = list(combinations(self, 2))

        for pair in coordinate_pairs:
            distance: float = pair[0].distance(pair[1])
            distance_dict[pair] = distance

        # Sort the dictionary by distance
        distance_dict = dict(sorted(distance_dict.items(), key=lambda item: item[1], reverse=False))

        return distance_dict
    
    def calculate_distance_matrix(self, boundary_conditions) -> np.array:

        n = len(self)
        distance_matrix: np.array = np.zeros((n, n))

        for i in range(n):
            for j in range(i+1, n):
                dist_x: float; dist_y: float; dist_z: float
                dist_x, dist_y, dist_z = self[i].distance(self[j])
                if boundary_conditions:
                    dist_x, dist_y, dist_z = self.__apply_boundary_conditions(dist_x, dist_y, dist_z)
                distance: float = math.sqrt(dist_x ** 2 + dist_y ** 2 + dist_z ** 2)
                distance_matrix[i][j] = distance
                distance_matrix[j][i] = distance

        return distance_matrix
    
    def to_array(self) -> np.array:

        data = list(map(
            lambda coordinate: coordinate.to_vector(),
            self
        ))

        return np.array(data)
    
    def to_dataframe(self) -> pd.DataFrame:

        data = list(map(
            lambda coordinate: [float(coordinate.x), float(coordinate.y), float(coordinate.z)],
            self
        ))

        data_frame = pd.DataFrame(data, columns=['x', 'y', 'z'])

        return data_frame
    
    def __apply_boundary_conditions(self, dist_x: float, dist_y: float, dist_z: float) -> List[float]:

        if dist_x > 1/2:
            dist_x = 1 - dist_x

        if dist_y > 1/2:
            dist_y = 1 - dist_y

        if dist_z > 1/2:
            dist_z = 1 - dist_z

        return [dist_x, dist_y, dist_z]