from gemmi import cif
from Crystal import Crystal
import os

data_directory = os.listdir("data")  # Directory where the data is stored


def user_input() -> str:
    while True:
        for index, item in enumerate(data_directory):
            print(index + 1, item)

        print(22 * "-")
        file_input = int(input("Enter the file number: "))
        if not (len(data_directory) >= file_input > 0):
            print("Index out of range, try again.")
            print("\n")
            continue
        file = data_directory[file_input - 1]
        path = "data/" + file
        print("Reading {}".format(file))
        return path


doc = cif.read_file(user_input())
crystal = Crystal(doc)

crystal.plot()
