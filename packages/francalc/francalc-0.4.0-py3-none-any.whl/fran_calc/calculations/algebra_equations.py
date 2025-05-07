from ..modules import run_test
from math import sqrt

def arithmetic_progression(a1, razao, termos):
    return [a1 + (i - 1) * razao for i in range(1, termos + 1)]

def geometric_progression(a1, razao, termos):
    return [a1 * (razao ** (i - 1)) for i in range(1, termos + 1)]

def solve_quadratic_equation(a, b, c):
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return "No real roots"
    elif discriminant == 0:
        x = -b / (2 * a)
        return [x]
    else:
        x1 = (-b + sqrt(discriminant)) / (2 * a)
        x2 = (-b - sqrt(discriminant)) / (2 * a)
        return [x1, x2]

def solve_linear_system(a1, b1, c1, a2, b2, c2): # 1,2,5,3,-5,4 | x = 3, y = 1
    # a1, b1, c1 = 1, 2, 5
    # a2, b2, c2 = 3, -5, 4
    # x + 2y = 5 | a1, b1, c1
    # 3x - 5y = 4 | a2, b2, c2
    # x = 3
    # y = 1
    denom = a1 * b2 - a2 * b1
    if denom == 0:
        return "No unique solution"
    x = (c1 * b2 - c2 * b1) / denom
    y = (a1 * c2 - a2 * c1) / denom
    return f"x = {x}, y = {y}"

if __name__ == "__main__":
    run_test(arithmetic_progression, 2, 7, 170)
    run_test(geometric_progression, 2, 7, 20)
    run_test(solve_quadratic_equation, 1, -3, 2)
    run_test(solve_linear_system, 1, 2, 5, 3, -5, 4)