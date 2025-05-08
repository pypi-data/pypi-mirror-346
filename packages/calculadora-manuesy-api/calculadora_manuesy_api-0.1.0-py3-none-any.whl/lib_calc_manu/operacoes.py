import math

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b) :
    return a * b


def divide(a, b) :
    if b == 0:
        raise ValueError("Divisão por zero não é permitida.")
    return a / b


def sqrt(a) :
    if a < 0:
        raise ValueError("A raiz quadrada de um número negativo não é real.")
    return math.sqrt(a)


def exponent(a, b) :
    return a ** b


def factorial(a) :
    return math.factorial(int(a))
