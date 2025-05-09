from .models import Operandos

def soma(operando: Operandos):
    return {"resultado": operando.num1 + operando.num2}

def subtracao(operando: Operandos):
    return {"resultado": operando.num1 - operando.num2}

def multiplicacao(operando: Operandos):
    return {"resultado": operando.num1 * operando.num2}

def divisao(operando: Operandos):
    if operando.num2 == 0:
        return {"erro": "Divisão por zero não é permitida."}
    return {"resultado": operando.num1 / operando.num2}

def potencia(operando: Operandos):
    return {"resultado": operando.num1 ** operando.num2}

def raiz(operando: Operandos):
    if operando.num1 < 0:
        return {"erro": "Raiz quadrada de número negativo não é permitida."}
    return {"resultado": operando.num1 ** (1 / operando.num2)}