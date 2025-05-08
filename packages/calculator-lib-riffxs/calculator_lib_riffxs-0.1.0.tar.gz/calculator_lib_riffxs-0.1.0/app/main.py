from fastapi import FastAPI, HTTPException

from app.models import OperationRequest, OperationResponse, OperationsEnum
from calculator-lib-riffxs import add, sub, mul, div

app = FastAPI()


@app.get('/')
async def read_root():
    return { "message": "Hello World" }

@app.post('/calc/{operation}', response_model=OperationResponse)
async def calculate(operation: OperationsEnum, request: OperationRequest):
    try:
        match (operation):
            case OperationsEnum.sum:
                result = add(request.a, request.b)

            case OperationsEnum.sub:
                result = sub(request.a, request.b)

            case OperationsEnum.mul:
                result = mul(request.a, request.b)

            case OperationsEnum.div:
                result = div(request.a, request.b)

        return OperationResponse(result=result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

