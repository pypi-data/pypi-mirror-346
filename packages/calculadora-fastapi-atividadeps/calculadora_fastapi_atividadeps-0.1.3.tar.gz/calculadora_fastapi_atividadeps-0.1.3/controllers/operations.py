# controllers/operations.py
from fastapi import APIRouter
from models.calculator import Calculator
from schemas.operation_request import OperationRequest

router = APIRouter()

@router.post("/add")
def add_numbers(request: OperationRequest):
    calc = Calculator(request.value1, request.value2)
    return {"result": calc.add()}

@router.post("/subtract")
def subtract_numbers(request: OperationRequest):
    calc = Calculator(request.value1, request.value2)
    return {"result": calc.subtract()}

@router.post("/multiply")
def multiply_numbers(request: OperationRequest):
    calc = Calculator(request.value1, request.value2)
    return {"result": calc.multiply()}

@router.post("/divide")
def divide_numbers(request: OperationRequest):
    calc = Calculator(request.value1, request.value2)
    return {"result": calc.divide()}