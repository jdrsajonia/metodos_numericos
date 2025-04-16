import sympy as sp #instalar con pip install
from math import *
import generate_table as table

def newtonRapshon(str_function, variable, point_k0, tolerance=0.0001):
    results={"k":[],"P_k":[],"(P_k+1)-(P_k)":[],"f(P_k)":[]}
    
    x = sp.Symbol(variable)
    # funciones simbolicas
    f_simbolic = sp.sympify(str_function) 
    f_diff_simbolic = sp.diff(f_simbolic, x) 

    # lambdify vuelve las funciones simbolicas en expresiones evaluables para Python
    f = sp.lambdify(x, f_simbolic, modules=["math"]) # f(x)
    f_diff = sp.lambdify(x, f_diff_simbolic, modules=["math"]) # f´(x) 
    k=0

    while True:
        f_pk=f(point_k0) # f(pk)
        f_diff_pk=f_diff(point_k0) # f´(pk)

        if f_diff_pk==0:
            break

        point_k1=point_k0-(f_pk/f_diff_pk)
        difference=abs(point_k1-point_k0)

        results["k"].append(k)
        results["P_k"].append(point_k0)
        results["(P_k+1)-(P_k)"].append(difference)
        results["f(P_k)"].append(f_pk)
        #print(f"{k} {point_k0:.6f} {point_k1 - point_k0:.6f} {f_pk:.6f} {f_diff_pk:.6f}")
        point_k0=point_k1
        
        if difference<tolerance:
            break
        k=k+1
    return results
    
def insert_function():
    while True:
        try:
            enter_funcion=input("\nIngresa una funcion en terminos de x, correctamente escrita en sintaxis de Python (usar 'math' si es necesario)\n---> f(x) = ")
            f = lambda x: eval(enter_funcion)
            resultado = f(1)
            return enter_funcion, f   
        except Exception as e:
            print(f"Función inválida: {e}")
            print("Por favor, intenta nuevamente.\n")

            
resultados=newtonRapshon("1980*(1-E**(-x/10))-98*x","x",16)
print(table.getTabla(resultados))
resultados = newtonRapshon("log(x) - 1", "x", 7)
print(table.getTabla(resultados))
resultados = newtonRapshon("E**x", "x", -8)
print(table.getTabla(resultados))


