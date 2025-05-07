from pydantic import BaseModel

class OperationRequest(BaseModel):
    """Modelo para requisições de operações matemáticas."""
    a: float
    b: float

class OperationResponse(BaseModel):
    """Modelo para respostas de operações matemáticas."""
    result: float
