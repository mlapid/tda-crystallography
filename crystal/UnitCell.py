import gemmi
from math import sin, cos, sqrt, pi


class UnitCell(gemmi.UnitCell):

    def __init__(self, a: float, b: float, c: float, alpha: float, beta: float, gamma: float):
        super().__init__(a, b, c, alpha, beta, gamma)

    def __repr__(self):
        return f'UnitCell({self.a}, {self.b}, {self.c}, {self.alpha}, {self.beta}, {self.gamma})'
    
    def __str__(self):
        return f'{self.a},{self.b},{self.c},{self.alpha},{self.beta},{self.gamma}'

    def calculate_volume(self) -> float:

        radians = pi / 180
        alpha_rad = self.alpha * radians
        beta_rad = self.beta * radians
        gamma_rad = self.gamma * radians

        volume = self.a * self.b * self.c * sqrt(1 + 2 * cos(alpha_rad) * cos(beta_rad) * cos(gamma_rad) -
                                  cos(alpha_rad)**2 - cos(beta_rad)**2 - cos(gamma_rad)**2
                                  )

        return volume
    
    def normalising_constant(self) -> float:

        return (1 / self.volume) ** (1/3)