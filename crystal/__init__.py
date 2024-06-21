import os

from gemmi import cif
from Crystal import Crystal
from typing import List
from tqdm import tqdm

data_path: str = "../crystal/data"
data_directory: List[str] = os.listdir(data_path)  # Directory where the data is stored


def user_input() -> str:
    while True:
        for index, item in enumerate(data_directory):
            print(index + 1, item)

        print(22 * "-")
        file_input: int = int(input("Enter the file number: "))
        if not (len(data_directory) >= file_input > 0):
            print("Index out of range, try again.")
            print("\n")
            continue
        file: str = data_directory[file_input - 1]
        path: str = data_path + "/" + file
        print("Reading {}".format(file))
        return path


# for index, file in tqdm(enumerate(data_directory[:1])):
#     path = data_path + "/" + file
#     doc = cif.read_file(path)
#     block = doc.sole_block()
#     crystal = Crystal(
#         block,
#         normalise=False,
#         boundary_conditions=False
#     )
#     print(crystal.unitCell.volume)
#     print(crystal.isNormalised)
#     print(crystal.normalising_constant)



doc = cif.read_file(user_input())
block = doc.sole_block()
crystal = Crystal(block)
print(crystal.unitCell.symmetries)
#
# crystal.plot()