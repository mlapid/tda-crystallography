'''Parse the AEI zeolite structure from a CIF file.'''

from pathlib import Path

from tda_crystallography.io import CifParser


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CIF_PATH = PROJECT_ROOT / 'data' / 'orthorhombic' / 'AEI.cif'


def main() -> None:
    parser = CifParser.from_file(CIF_PATH)

    print(f'Crystal: {parser.crystal_name}')
    print(f'System:  {parser.crystal_system}')
    print(f'Space group: {parser.space_group}')
    print(f'Unit cell: {parser.unit_cell}')
    print(f'Symmetry operations: {len(parser.symmetries)}')
    print(f'Atoms in asymmetric unit: {len(parser.atom_sites)}')

    print('\nFractional coordinates:')
    for coordinate in sorted(
        parser.atom_sites,
        key=lambda c: (c.x, c.y, c.z),
    ):
        print(f'  {coordinate}')

    print('\nFirst atom in Cartesian coordinates:')
    coordinate = next(iter(parser.atom_sites))
    positional = coordinate.to_positional_atom(parser.unit_cell)
    print(f'  fractional: {coordinate}')
    print(f'  positional: {positional}')


if __name__ == '__main__':
    main()