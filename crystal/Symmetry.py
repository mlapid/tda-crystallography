import gemmi
import numpy as np
from fractions import Fraction
from Fractional import FractionalCoordinate, FractionalCoordinateList

class Symmetry(gemmi.Op):

    def __init__(self, symmetry: str) -> None:
        super().__init__(symmetry)

        self.order = self.__get_order()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.triplet()})'
    
    def __str__(self) -> str:
        return f'{self.triplet()}'

    def __get_order(self) -> int:

        symmetry = self

        n = 1

        while symmetry.triplet() != 'x,y,z':
            symmetry = self * symmetry
            n += 1

        return n

    def apply_to_fractional_coordinate(self, coordinate: FractionalCoordinate) -> FractionalCoordinateList:
        
        fractionalCoordinateList: FractionalCoordinateList = FractionalCoordinateList()
        fractionalCoordinateList.append(coordinate)

        for _ in range(self.order - 1):
            x_prime: np.array = np.array(self.seitz()) @ np.append(coordinate.to_vector(), Fraction(1))
            x, y, z, _ = x_prime
            coordinate = FractionalCoordinate(x, y, z)
            fractionalCoordinateList.append(coordinate)
        
        return fractionalCoordinateList
    
    # def apply_to_fractional_coordinate_list(self, fractionalCoordinateList: FractionalCoordinateList) -> FractionalCoordinateList:

    #     updatedFractionalCoordinateList: FractionalCoordinateList = FractionalCoordinateList()

    #     for coordinate in fractionalCoordinateList:
    #         updatedFractionalCoordinateList.extend(self.apply_to_fractional_coordinate(coordinate))

    #     return updatedFractionalCoordinateList