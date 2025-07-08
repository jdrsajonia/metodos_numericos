import ShootingLineal as dl
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np 
import time

def parse_str_function(x_function:str):
    """
    funcion correspondiente a la solución de x(t) de una ecuación diferencial
    de la forma mx''(t) + cx'(t) + kx(t) - g(t) = 0

    x_function: es un string que representa una función x en términos de t.

    returns: la función evaluable
    """

    t=sp.symbols("t")
    algebraic_function=sp.sympify(x_function)
    eval_x_function=sp.lambdify(t, algebraic_function)

    return eval_x_function




def graphic_solution(data: dict, x_function_str: str):
    """
    Grafica los puntos de la solución numérica (t_k, x_k) y la curva analítica x(t).

    Args:
        data (dict): Diccionario con llaves "t_k" y "x_k" que representan la solución numérica.
        x_function_str (str): String que representa la función x(t) exacta.
    """

    # Extrae puntos
    t_points = np.array(data["t_k"])
    x_points = np.array(data["x_k"])

    # Evalúa función analítica
    x_function = parse_str_function(x_function_str)
    t_continuo = np.linspace(min(t_points), max(t_points), 300)
    x_continuo = x_function(t_continuo)

    # Graficar
    plt.figure(figsize=(10, 6))
    plt.scatter(t_points, x_points, color='red', label='Solución numérica (RK4)', zorder=5)
    plt.plot(t_continuo, x_continuo, color='blue', label='Solución analítica', linewidth=2)

    plt.title('Comparación: Solución Analítica vs Numérica (Método de Disparo)', fontsize=14)
    plt.xlabel('t', fontsize=12)
    plt.ylabel('x(t)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()


func_example=parse_str_function("1.25 + 0.4860896526*t - 2.25*t**2 + 2*t*arctan(t) + (1/2)*(t**2-1)*ln(1+t**2)")


ecuation=dl.ShootLineal("ddx - ((2*t)/(1+t**2))*dx + (2/(1+t**2))*x - 1", (0,4), 0.2, 1.25, -0.95)

init=time.perf_counter()
results=ecuation.solve_by_shoot()
end=time.perf_counter()

print(f" Tiempo de ejecucion: {end-init}")

func="1.25 + 0.4860896526*t - 2.25*t**2 + 2*t*arctan(t) + (1/2)*(t**2-1)*ln(1+t**2)"

graphic_solution(results,func)
print(func_example(1.6))