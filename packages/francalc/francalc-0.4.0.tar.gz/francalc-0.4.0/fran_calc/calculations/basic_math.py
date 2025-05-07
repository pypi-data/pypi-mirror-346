from ..modules import safe_eval, run_test
from math import sqrt, factorial, gcd, lcm

def simple_arithmetic(expr: str):
    OP_MAP = {
        'add': '+',
        'sub': '-',
        'mul': '*',
        'truediv': '/',
        'floordiv': '//',
        'pow': '**',
        'mod': '%',
    }

    tokens = expr.split()
    # Troca cada token conhecido pelo seu símbolo
    py_tokens = [OP_MAP.get(tok, tok) for tok in tokens]
    py_expr = ' '.join(py_tokens)
    return safe_eval(py_expr)

def calculate_sqrt(radicando: int):
    if radicando < 0:
        raise ValueError("Raiz quadrada de número negativo não é real")
    return sqrt(radicando)

def calculate_factorial(numero: int):
    if numero < 0:
        raise ValueError("Número negativo não tem fatorial")
    return factorial(numero)

def calculate_percentage(part, total):
    return f"{part / total:.2%}"

def calculate_average(valores):
    numeros_str = valores
    numeros = [float(x.strip()) for x in numeros_str.split(',')]
    soma = sum(numeros)
    media = soma / len(numeros)
    return media

def find_min_and_max(valores):
    if isinstance(valores, (list, tuple)):
        nums = [float(v) for v in valores]
    else:
        nums = [float(x.strip()) for x in str(valores).split(',') if x.strip()]
    return f'Mínimo: {int(min(nums))}, Máximo: {int(max(nums))}'

def calculate_lcm(*valores):
    # coleta todos os números, seja int, str "a,b,c" ou lista/tupla
    nums = []
    for v in valores:
        if isinstance(v, str):
            nums.extend(int(x) for x in v.split(',') if x.strip())
        elif isinstance(v, (list, tuple)):
            nums.extend(int(x) for x in v)
        else:
            nums.append(int(v))
    # calcula LCM em cadeia
    resultado = nums[0]
    for n in nums[1:]:
        resultado = lcm(resultado, n)
    return resultado
def calculate_gcd(*valores):
    # coleta todos os números, seja int, str "a,b,c" ou lista/tupla
    nums = []
    for v in valores:
        if isinstance(v, str):
            nums.extend(int(x) for x in v.split(',') if x.strip())
        elif isinstance(v, (list, tuple)):
            nums.extend(int(x) for x in v)
        else:
            nums.append(int(v))
    # calcula GCD em cadeia
    resultado = nums[0]
    for n in nums[1:]:
        resultado = gcd(resultado, n)
    return resultado

def check_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def int_to_roman(num):
    if not (0 < num < 4000):
        raise ValueError("Número fora do intervalo (1-3999)")
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syms = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syms[i]
            num -= val[i]
        i += 1
    return roman_num

if __name__ == "__main__":
    # simple_arithmetic("add 3 mul 5 sub 2 truediv 8 pow 4 mod 2")
    run_test(simple_arithmetic, "1+2**3")
    run_test(calculate_percentage, 50, 200)
    run_test(calculate_average, "1, 2, 3, 4, 5")
    run_test(find_min_and_max, "1, 2, 3, 4, 5")
    run_test(calculate_lcm, 7, 14, 21) # calculate_lcm(7, 14, 21) = 42
    run_test(calculate_gcd, 7, 14, 21)
    run_test(check_prime, 7)
    run_test(int_to_roman, 3999)