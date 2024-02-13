import gemmi
from gemmi import cif, Op, Fractional
import numpy as np
import pandas as pd
from Atom import Atom
from AtomList import AtomList


class UnitCell:

    def __init__(self, block: cif.Block):
        self.block = block

        self.cell = self.__get_unit_cell()
        self.symmetries = self.__get_symmetries()
        self.fractionalCoordinates = self.__extend_fractional_coordinates()
        self.cartesianCoordinates = self.__get_cartesian_coordinates()

    def __repr__(self):
        return f'{self.cell.a, self.cell.b, self.cell.c, self.cell.alpha, self.cell.beta, self.cell.gamma}'

    def __get_unit_cell(self) -> gemmi.UnitCell:
        block = self.block

        cutoff = 7

        length_a = float(block.find_value('_cell_length_a')[:cutoff])
        length_b = float(block.find_value('_cell_length_b')[:cutoff])
        length_c = float(block.find_value('_cell_length_c')[:cutoff])

        angle_alpha = float(block.find_value('_cell_angle_alpha')[:cutoff])
        angle_beta = float(block.find_value('_cell_angle_beta')[:cutoff])
        angle_gamma = float(block.find_value('_cell_angle_gamma')[:cutoff])

        cell = gemmi.UnitCell(length_a, length_b, length_c, angle_alpha, angle_beta, angle_gamma)

        return cell

    def __get_symmetries(self) -> list:
        symmetries = [Op(s.strip('"\'')) for s in self.block.find_values('_symmetry_equiv_pos_as_xyz')]

        return symmetries

    def __get_initial_coordinates(self) -> AtomList:
        block = self.block

        initial_coordinates = AtomList()

        # label = block.find_values('_atom_site_label')
        symbol = block.find_values('_atom_site_type_symbol')
        col_x = block.find_values('_atom_site_fract_x')
        col_y = block.find_values('_atom_site_fract_y')
        col_z = block.find_values('_atom_site_fract_z')

        coordinate_array = np.array([
            [float(i) for i in col_x],
            [float(i) for i in col_y],
            [float(i) for i in col_z]
        ], dtype='float16').transpose()

        # label = [str(i) for i in label]
        symbol = [str(i) for i in symbol]

        for index, row in enumerate(coordinate_array):
            coordinate = Fractional(row[0], row[1], row[2])
            atom_symbol = symbol[index]
            atom = Atom(coordinate, atom_symbol)
            initial_coordinates.append(atom)

        return initial_coordinates

    def __extend_fractional_coordinates(self) -> AtomList:
        initial_coordinates = self.__get_initial_coordinates()

        fractional_coordinates = AtomList()

        for atom in initial_coordinates:
            fractional_coordinates.append(atom)
            symbol = atom.symbol
            for sym in self.symmetries:
                new_coordinates = sym.apply_to_xyz(atom.coordinates.tolist())
                new_coordinates = Fractional(
                    new_coordinates[0], new_coordinates[1], new_coordinates[2]
                ).wrap_to_unit()
                new_atom = Atom(new_coordinates, symbol)
                fractional_coordinates.append(new_atom)

        return fractional_coordinates

    def __get_cartesian_coordinates(self) -> AtomList:
        # Transform into Cartesian coordinate system

        cartesian_coordinates = AtomList()

        for atom in self.fractionalCoordinates:
            coordinates = atom.coordinates
            symbol = atom.symbol
            new_coordinates = self.cell.orthogonalize(coordinates)  # Position
            cartesian_coordinates.append(Atom(new_coordinates, symbol))

        return cartesian_coordinates

    def to_dataframe(self) -> pd.DataFrame:

        data = list(map(
            lambda atom: atom.coordinates.tolist() + [atom.symbol],
            self.cartesianCoordinates
        ))

        df = pd.DataFrame(data, columns=['x', 'y', 'z', 'symbol'])

        return df