from fastapi import FastAPI, HTTPException
from app.models import OperationRequest, OperationResponse, SingleNumberRequest
from calculator_lib import add, subtract, multiply, divide, square_root, power

app = FastAPI(
    title="FastAPI Calculator",
    description="📟 Uma API de Calculadora Simples feita com FastAPI e usando a Lib (Calculadora Lib) \n\nSuporta operações de adição, subtração, multiplicação, divisão, raiz quadrada e exponenciação.",
    version="1.1.0"
)

example_request = {
    "a": 10,
    "b": 5
}

example_single_request = {
    "x": 9
}

@app.post("/add", response_model=OperationResponse, summary="Adição", description="Soma dois números.")
def add_numbers(request: OperationRequest):
    """
    Soma dois números enviados na requisição.
    """
    result = add(request.a, request.b)
    return OperationResponse(result=result)

@app.post("/subtract", response_model=OperationResponse, summary="Subtração", description="Subtrai dois números.")
def subtract_numbers(request: OperationRequest):
    """
    Subtrai dois números enviados na requisição.
    """
    result = subtract(request.a, request.b)
    return OperationResponse(result=result)

@app.post("/multiply", response_model=OperationResponse, summary="Multiplicação", description="Multiplica dois números.")
def multiply_numbers(request: OperationRequest):
    """
    Multiplica dois números enviados na requisição.
    """
    result = multiply(request.a, request.b)
    return OperationResponse(result=result)

@app.post("/divide", response_model=OperationResponse, summary="Divisão", description="Divide dois números.")
def divide_numbers(request: OperationRequest):
    """
    Divide dois números enviados na requisição.
    """
    try:
        result = divide(request.a, request.b)
        return OperationResponse(result=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/sqrt", response_model=OperationResponse, summary="Raiz Quadrada", description="Calcula a raiz quadrada de um número.")
def sqrt_number(request: SingleNumberRequest):
    """
    Calcula a raiz quadrada de um número.
    """
    try:
        result = square_root(request.x)
        return OperationResponse(result=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/power", response_model=OperationResponse, summary="Exponenciação", description="Calcula a potência de um número (base elevada ao expoente).")
def power_numbers(request: OperationRequest):
    """
    Calcula a potência de um número (base elevada ao expoente).
    """
    result = power(request.a, request.b)
    return OperationResponse(result=result)