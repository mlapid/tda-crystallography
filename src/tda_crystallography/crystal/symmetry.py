import gemmi
from pydantic.config import ConfigDict
from pydantic import BaseModel, field_validator


class Symmetry(BaseModel):
    model_config = ConfigDict(
        title='Symmetry',
        frozen=True,
        arbitrary_types_allowed=True
    )
    
    operation: gemmi.Op

    @field_validator('operation', mode='before')
    def validate_operation(cls, operation: str | gemmi.Op) -> gemmi.Op:
        if isinstance(operation, gemmi.Op):
            return operation

        return gemmi.Op(operation)
    
    def __str__(self) -> str:
        return self.operation.triplet()
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.operation.triplet()!r})'
    
    @property
    def order(self) -> int:

        operation: gemmi.Op = self.operation

        n = 1

        while operation.triplet() != 'x,y,z':
            operation = self.operation * operation
            n += 1

        return n
