from fastapi import FastAPI
from .models import Operandos
from .operations import soma, subtracao, multiplicacao, divisao, potencia, raiz

app = FastAPI()

@app.post("/soma")
def somaRoute(operando: Operandos):
    return soma(operando)

@app.post("/subtracao")
def subtracaoRoute(operando: Operandos):
    return subtracao(operando)

@app.post("/multiplicacao")
def multiplicacaoRoute(operando: Operandos):
    return multiplicacao(operando)

@app.post("/divisao")
def divisaoRoute(operando: Operandos):
    return divisao(operando)

@app.post("/potencia")
def potenciaRoute(operando: Operandos):
    return potencia(operando)

@app.post("/raiz")
def raizRoute(operando: Operandos):
    return raiz(operando)
