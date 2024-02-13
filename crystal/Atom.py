import gemmi


class Atom:

    def __init__(self, coordinates: gemmi.Vec3, symbol: str):
        self.coordinates = coordinates
        self.symbol = symbol

    def __str__(self):
        return f'{self.symbol} atom with coordinates {self.coordinates}'

    def __repr__(self):
        return f'{self.coordinates}, {self.symbol}'

    def is_equal(self, other) -> bool:
        if (self.coordinates.x == other.coordinates.x) and \
                (self.coordinates.y == other.coordinates.y) and \
                (self.coordinates.z == other.coordinates.z) and \
                (self.symbol == other.symbol):
            return True
        else:
            return False
