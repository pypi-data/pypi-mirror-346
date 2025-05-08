# schemas/operation_request.py
from pydantic import BaseModel

class OperationRequest(BaseModel):
    value1: float
    value2: float