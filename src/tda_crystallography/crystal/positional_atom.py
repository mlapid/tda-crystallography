from typing import Annotated

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from tda_crystallography.crystal.positional_coordinate import PositionalCoordinate


class PositionalAtom(BaseModel):
    model_config = ConfigDict(
        title='PositionalAtom',
        frozen=True,
        arbitrary_types_allowed=False
    )

    label: Annotated[str, Field(description='The label of the atom.')]
    element: Annotated[str, Field(description='The chemical element of the atom.')]
    positional_coordinate: PositionalCoordinate

    def __str__(self) -> str:
        return (
            f'{self.__class__.__name__}'
            f'(label={self.label!r}, element={self.element!r}, positional_coordinate={self.positional_coordinate})'
        )
    
    def __repr__(self) -> str:
        return self.__str__()