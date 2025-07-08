import sympy as sp
import numpy as np 
import matplotlib.pyplot as plt


def parse_str_function(x_function:str):
    """
    Convierte un string que representa una función de x(t)
    en una función evaluable en t.

    Args:
        x_function (str): Expresión algebraica como string dependiente de t.

    Returns:
        function: Función evaluable en t.
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

    # extrae puntos
    t_points=np.array(data["t_k"])
    x_points=np.array(data["x_k"])

    # evalúa función analítica
    x_function=parse_str_function(x_function_str)
    t_continuo=np.linspace(min(t_points), max(t_points), 300)
    x_continuo=x_function(t_continuo)

    # graficar
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

def get_comparative_results(results:dict, x_function:str):
    """
    Agrega al diccionario de resultados los valores exactos x(t_k)
    y el error entre la solución exacta y la aproximada.

    Args:
        results (dict): Diccionario con claves "t_k" y "x_k".
        x_function (str): Solución exacta de x(t) como string.

    Returns:
        dict: Diccionario extendido con:
            - "x(t_k) exacto"
            - "x(t_k) exacto - x_k (error)"
    """
    eval_x_function=parse_str_function(x_function)
    t_k_list=results["t_k"]
    results["x(t_k) exacto"]=[eval_x_function(t_k) for t_k in t_k_list]
    results["x(t_k) exacto - x_k (error)"]=[x_exacto - x_aprox for x_exacto, x_aprox in zip(results["x(t_k) exacto"], results["x_k"])]
    return results
    




