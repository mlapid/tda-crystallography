import gemmi


class Atom:

    def __init__(self, coordinates: gemmi.Vec3, symbol: str):
        self.coordinates = coordinates
        self.symbol = symbol

    def __str__(self):
        return f'{self.symbol} atom with coordinates {self.coordinates}'

    def __repr__(self):
        return f'{self.coordinates}, {self.symbol}'

    def __eq__(self, other) -> bool:
        if (self.coordinates.x == other.coordinates.x) and \
                (self.coordinates.y == other.coordinates.y) and \
                (self.coordinates.z == other.coordinates.z) and \
                (self.symbol == other.symbol):
            return True
        else:
            return False

    def distance(self, other):

        dist_x: float = abs(self.coordinates.x - other.coordinates.x)
        dist_y: float = abs(self.coordinates.y - other.coordinates.y)
        dist_z: float = abs(self.coordinates.z - other.coordinates.z)

        return dist_x, dist_y, dist_z
