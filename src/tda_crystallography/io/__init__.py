from pathlib import Path

from tda_crystallography.io.cif_parser import CifParser
from tda_crystallography.crystal.crystal import Crystal


def parse_cif(path: str | Path, *, block_name: str | None = None) -> Crystal:
    return CifParser.from_file(path=path, block_name=block_name).parse()

__all__ = ['CifParser', 'parse_cif']