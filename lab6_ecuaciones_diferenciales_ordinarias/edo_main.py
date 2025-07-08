import sympy as sp
import ShootingLineal as sl
import utils_functions as utils
import time 
import getTabla as t
def user_input():
    """
    Solicita al usuario la ecuación diferencial, el intervalo, el paso h y las condiciones alpha y beta.
    Valida cada entrada asegurando el formato correcto.
    """

    print("="*62+"\nSolución de problemas de contorno para EDOs con Disparo Lineal\n"+"="*62)
    print()

    while True:
        try:
            print("Ingrese la ecuación en formato: m*ddx + c*dx + k*x - g")
            ecuation=input("EDO = 0 >> ")
            expr=sp.sympify(ecuation)
            if not any(s in ecuation for s in ["ddx", "dx", "x"]):
                raise ValueError("La ecuación debe contener ddx, dx y x.\n")
            break
        except Exception as e:
            print("Error:", e, "-> Intente de nuevo.\n")
    print("\nIngrese el intervalo [a,b]")
    while True:
        try:
            a=float(input("a >> "))
            b=float(input("b >> "))
            if a >= b:
                raise ValueError("a debe ser menor que b.\n")
            interval=(a,b)
            break
        except Exception as e:
            print("Error:", e, "-> Intente de nuevo.\n")
    print("\nPaso de integración h:")
    while True:
        try:
            h=float(input("h >> "))
            if h <= 0 or h >= (b - a):
                raise ValueError("h debe ser positivo y menor que (b - a).\n")
            break
        except Exception as e:
            print("Error:", e, "-> Intente de nuevo.\n")
    print("\nCondición inicial y(a) = alpha")
    while True:
        try:
            alpha=float(input("alpha >> "))
            break
        except Exception as e:
            print("Error:", e, "-> Intente de nuevo.\n")
    print("\nCondición inicial y(b) = betha")
    while True:
        try:
            beta=float(input("betha >> "))
            break
        except Exception as e:
            print("Error:", e, "-> Intente de nuevo.\n")

    return ecuation, interval, h, alpha, beta

def main(ecuation:str=None, interval:tuple=None, h_steps:float=None, alpha:float=None, betha:float=None, exact_solution=None, user_console=True, ):

    if user_console:
        ecuation, interval, h_steps, alpha, betha = user_input()
    
    contour_problem=sl.ShootLineal(ecuation, interval, h_steps, alpha, betha)

    init=time.perf_counter()
    results=contour_problem.solve_by_shoot()
    end=time.perf_counter()

    if exact_solution:
        results=utils.get_comparative_results(results,exact_solution)

    print(t.getTabla(results, setTitle=f"Valores de solución en {contour_problem.ecuation} con h = {h_steps}"))

    print(f"\nTiempo de ejecución: {end-init}")

    utils.graphic_solution(results, exact_solution)

    

# main("ddx - ((2*t)/(1+t**2))*dx + (2/(1+t**2))*x - 1", (0,4), 0.2, 1.25, -0.95, exact_solution="1.25 + 0.4860896526*t - 2.25*t**2 + 2*t*arctan(t) + (1/2)*(t**2-1)*ln(1+t**2)", user_console=False)
