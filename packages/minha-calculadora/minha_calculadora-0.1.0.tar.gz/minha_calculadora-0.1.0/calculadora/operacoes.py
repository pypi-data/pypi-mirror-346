# minha_calculadora/calculadora/operacoes.py

from fastapi import HTTPException

def somar(number1: float, number2: float) -> float:
    return number1 + number2

def subtrair(number1: float, number2: float) -> float:
    return number1 - number2

def multiplicar(number1: float, number2: float) -> float:
    return number1 * number2

def dividir(number1: float, number2: float) -> float:
    if number2 == 0:
        raise HTTPException(status_code=400, detail="Divisão por zero não permitida.")
    return number1 / number2

def exponenciar(number1: float, number2: float) -> float:
    return number1 ** number2

def radiciacao(number1: float, number2: float) -> float:
    if number2 == 0:
        raise HTTPException(status_code=400, detail="Índice da raiz não pode ser zero.")
    return number1 ** (1 / number2)