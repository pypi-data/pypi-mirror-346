def soma(num1: float, num2: float) -> float:
    return num1 + num2

def subs(num1: float, num2: float) -> float:
    return num1 - num2

def mult(num1: float, num2: float) -> float:
    return num1 * num2

def divs(num1: float, num2: float) -> float:
    if (num2 == 0):
        raise ValueError("Divisão por Zero")
    
    return num1 / num2

def powX(num1: float, num2: float) -> float:
    return num1 ** num2

def pow2(num1: float) -> float:
    return num1 ** 2

def raiz(num1: float, num2: float) -> float:
    if (num2 == 0):
        raise ValueError("Expoente Zero")
    
    return num1 ** (1/num2)

def rzqd(num1: float) -> float:
    return num1 ** (1/2)