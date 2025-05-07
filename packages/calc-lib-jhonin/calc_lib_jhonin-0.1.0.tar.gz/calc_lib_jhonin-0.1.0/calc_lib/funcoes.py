def adicao(a: float, b: float) -> float:
    return a + b

def subtracao(a: float, b: float) -> float:
    return a - b

def multiplicacao(a: float, b: float) -> float:
    return a * b

def divisao(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Divisão por zero não é permitida.")
    return a / b

def potencia(a: float, b: float) -> float:
    return a ** b

def raiz(a: float, b: float) -> float:
    if (a < 0 and b % 2 == 0):
        raise ValueError("Raiz par de número negativo não é permitida.")
    if b == 0:
        raise ValueError("Raiz de zero não é permitida.")
    return a ** (1/b)
    