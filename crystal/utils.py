import gemmi
import numpy as np
import pandas as pd
import plotly.express as px

from gudhi.wasserstein import wasserstein_distance

from Fractional import FractionalCoordinate, FractionalCoordinateList
from typing import List
from random import random, randint
from fractions import Fraction
from tqdm import tqdm

def generate_random_fractional_coordinates(n: int) -> FractionalCoordinateList:
    
    fractionalCoordinates: FractionalCoordinateList = FractionalCoordinateList()
    
    for _ in range(n):

        x: Fraction = Fraction(random())
        y: Fraction = Fraction(random())
        z: Fraction = Fraction(random())

        fractionalCoordinates.append(FractionalCoordinate(x, y, z))
    
    return fractionalCoordinates

def transform_persistence_intervals(persistence: List[np.array]) -> List[tuple]:
    # Transform ripser persistence to gudhi persistence
    persistence_list: List[tuple] = []

    for dim, array in enumerate(persistence):
        for interval in array:
            persistence_list.extend([(dim, tuple(interval))])
    
    return persistence_list

def wasserstein_distance_matrix(crystals: dict, dimension: int) -> pd.DataFrame:

    '''
    crystals = {'Code': {'persistence': np.array}
    '''

    crystal_list: List[str] = list(crystals.keys())
    n: int = len(crystal_list)

    distance_matrix: pd.DataFrame = pd.DataFrame(data = np.zeros((n, n)), index = crystal_list, columns = crystal_list)

    for i in tqdm(range(n)):
        for j in range(i+1, n):
            crystal_A: str = crystal_list[i]
            crystal_B: str = crystal_list[j]

            persistence_A: np.array = crystals[crystal_A]['persistence'][dimension]
            persistence_B: np.array = crystals[crystal_B]['persistence'][dimension]

            persistence_A = np.array(list(filter(lambda i: i[1] < float('inf'), persistence_A)))
            persistence_B = np.array(list(filter(lambda i: i[1] < float('inf'), persistence_B)))

            wd = round(wasserstein_distance(
                persistence_A, persistence_B
                ), 4)
            
            distance_matrix.loc[crystal_A, crystal_B] = wd
            distance_matrix.loc[crystal_B, crystal_A] = wd

    return distance_matrix

def plot_distance_matrix(distance_matrix: pd.DataFrame) -> None:

    fig = px.imshow(
            img = distance_matrix.values,
            x = distance_matrix.columns,
            y = distance_matrix.index,
            labels = dict(color = "Distance"),
            color_continuous_scale = "Blues",
            text_auto = ".2f",
            aspect = "auto"
            )
    fig.update_layout(
        title = "Wasserstein Distance Matrix"
    )
    fig.show()