from fastapi import FastAPI, HTTPException
from application.models import OperationRequest, OperationResponse
from calc_lib_jonathancastrosilva import adicao, subtracao, multiplicacao, divisao
from calc_lib.funcoes import potencia, raiz

app = FastAPI(title="Calculadora API")

example_request = {
    "a": 10,
    "b": 5
}

@app.post("/adicao", response_model=OperationResponse, summary="Adição", description="adição de dois números.")
def adicao_num(request: OperationRequest):
    resultado = adicao(request.a, request.b)
    return OperationResponse(result=resultado)

@app.post("/subtracao", response_model=OperationResponse, summary="Subtração", description="subtração de dois números.")
def subtracao_num(request: OperationRequest):
    resultado = subtracao(request.a, request.b)
    return OperationResponse(result=resultado)

@app.post("/multiplicacao", response_model=OperationResponse, summary="Multiplicação", description="multiplicação de dois números.")
def multiplicacao_num(request: OperationRequest):
    resultado = multiplicacao(request.a, request.b)
    return OperationResponse(result=resultado)

@app.post("/divisao", response_model=OperationResponse, summary="Divisão", description="Divisão de dois números.")
def divisao_num(request: OperationRequest):
    try:
        resultado = divisao(request.a, request.b)
        return OperationResponse(result=resultado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/potencia", response_model=OperationResponse, summary="Potência", description="Potência de dois números.")
def potencia_num(request: OperationRequest):
    resultado = potencia(request.a, request.b)
    return OperationResponse(result=resultado)

@app.post("/raiz", response_model=OperationResponse, summary="Raiz", description="Raiz de dois números.")
def raiz_num(request: OperationRequest):
    try:
        resultado = raiz(request.a, request.b)
        return OperationResponse(result=resultado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))