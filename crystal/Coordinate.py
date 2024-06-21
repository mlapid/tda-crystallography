from abc import ABC, abstractmethod
from typing import Self
import gemmi

class Coordinate(ABC):
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    @abstractmethod
    def __str__(self) -> str:
        pass

    def __eq__(self, coordinate: Self) -> bool:
        if (self.x == coordinate.x and \
             self.y == coordinate.y and \
            self.z == coordinate.z):
            return True
        else:
            return False


class FractionalCoordinate(Coordinate, gemmi.Fractional):
    def __init__(self, x: float, y: float, z: float):
        Coordinate.__init__(self, x, y, z)
        gemmi.Fractional.__init__(self, x, y, z)

    def __str__(self) -> str:
        return f'Fractional coordinates: {self.x}, {self.y}, {self.z}'