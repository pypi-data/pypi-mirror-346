from enum import Enum
from pydantic import BaseModel


class OperationRequest(BaseModel):
    a: float
    b: float

class OperationResponse(BaseModel):
    result: float

class OperationsEnum(Enum):
    sum = "add"
    sub = "subtract"
    mul = "multiply"
    div = "divide"

