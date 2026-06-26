from typing import Annotated

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from tda_crystallography.crystal.unit_cell import UnitCell
from tda_crystallography.crystal.positional_atom import PositionalAtom
from tda_crystallography.crystal.fractional_coordinate import FractionalCoordinate
from tda_crystallography.crystal.positional_coordinate import PositionalCoordinate


class Atom(BaseModel):
    model_config = ConfigDict(
        title='Atom',
        frozen=True,
        arbitrary_types_allowed=False
    )

    label: Annotated[str, Field(description='The label of the atom.')]
    element: Annotated[str, Field(description='The chemical element of the atom.')]
    fractional_coordinate: FractionalCoordinate

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}'
            f'(label={self.label!r}, element={self.element!r}, fractional_coordinate={self.fractional_coordinate})'
        )
    
    def __repr__(self) -> str:
        return self.__str__()

    def to_positional_atom(
        self,
        unit_cell: UnitCell,
        *,
        normalise: bool = False,
    ) -> PositionalAtom:
        positional_coordinate: PositionalCoordinate = self.fractional_coordinate.orthogonalise(unit_cell)
        
        if normalise:
            positional_coordinate = positional_coordinate.normalise(unit_cell.normalising_constant)

        return PositionalAtom(
            label=self.label,
            element=self.element,
            positional_coordinate=positional_coordinate,
        )