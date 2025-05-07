from fastapi import FastAPI, HTTPException
from .models import OperationRequest, OperationResponse
from lib import sum, subtract, multiply, divide, power, square_root


app = FastAPI()

@app.post("/add")
def sum_endpoint(operation: OperationRequest):
    return OperationResponse(result=sum(operation.a, operation.b))

@app.post("/subtract")
def subtraction_endpoint(operation: OperationRequest):
    return OperationResponse(result=subtract(operation.a, operation.b))

@app.post("/multiply")
def multiply_endpoint(operation: OperationRequest):
    return OperationResponse(result=multiply(operation.a, operation.b))

@app.post("/divide")
def divide_endpoint(operation: OperationRequest):
    if operation.b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed")
    return OperationResponse(result=divide(operation.a, operation.b))

@app.post("/power")
def power_endpoint(operation: OperationRequest):
    return OperationResponse(result=power(operation.a, operation.b))

@app.post("/square_root")
def square_root_endpoint(operation: OperationRequest):
    if operation.a < 0:
        raise HTTPException(status_code=400, detail="Square root of negative number is not allowed")
    return OperationResponse(result=square_root(operation.a))

def main():
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)