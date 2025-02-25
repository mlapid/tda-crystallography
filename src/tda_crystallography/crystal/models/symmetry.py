import gemmi
from pydantic.config import ConfigDict
from pydantic import BaseModel, Field, field_validator

class Symmetry(BaseModel):
    model_config = ConfigDict(
        title='Symmetry',
        frozen=True,
        arbitrary_types_allowed=True
    )
    
    operation: gemmi.Op

    @field_validator('operation', mode='before')
    @classmethod
    def validate_operation(cls, operation: str) -> gemmi.Op:
        return gemmi.Op(operation)
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}(operation={self.operation.triplet()}, order={self.order})'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def order(self) -> int:

        operation = self.operation

        n = 1

        while operation.triplet() != 'x,y,z':
            operation = self.operation * operation
            n += 1

        return n
    
