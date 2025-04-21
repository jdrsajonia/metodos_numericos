import sympy as sp # instalar con pip install dado el caso
import matplotlib.pyplot as plt
import numpy as np


def newtonRaphson(str_function, variable, point_k0, tolerance=0.0001, decimal_notation=False):
    """
    Implementa el metodo de Newton-Raphson para encontrar raices de funciones continuas.

    Parametros:
        str_function (str): Expresion de la funcion, en formato string (por ejemplo, "x**2 - 2").
        variable (str): Variable simbolica usada en la funcion (por ejemplo, "x").
        point_k0 (float): Punto inicial de la iteracion.
        tolerance (float, optional): Criterio de tolerancia para detener las iteraciones. Default es 0.0001.
        decimal_notation (bool, optional): Si es True, convierte los resultados numericos a notacion decimal (8 decimales). Default es False.

    Returns:
        dict: Diccionario con claves:
            - "k": Numero de iteracion.
            - "P_k *root*": Valor actual de la raiz estimada.
            - "(P_k+1)-(P_k)": Diferencia entre iteraciones.
            - "f(P_k)": Valor de la funcion en el punto actual.

    Nota:
        Se usan funciones simbolicas y derivadas automaticas con SymPy.
        Si la derivada es 0 en algun punto, se detiene el metodo para evitar division por cero.
    """
    results={"k":[],"P_k *root*":[],"(P_k+1)-(P_k)":[],"f(P_k)":[]}

    def fmt(value): # funcion interna que formatea los datos de results en decimales (opcional) 
        return f"{value:.8f}" if decimal_notation else value
    
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

        if f_diff_pk==0: # evita la division por cero
            break 

        point_k1=point_k0-(f_pk/f_diff_pk) # newton-raphson formula
        difference=abs(point_k1-point_k0)

        results["k"].append(k)
        results["P_k *root*"].append(fmt(point_k0))
        results["(P_k+1)-(P_k)"].append(fmt(difference))
        results["f(P_k)"].append(fmt(f_pk))

        point_k0=point_k1 # se actualiza al siguiente punto
        
        if difference<tolerance:
            break
        k=k+1
    return results

def process_function(str_function, str_variable):
    """
    Convierte una funcion dada como string a una funcion evaluable en Python.

    Args:
        str_function (str): Expresion de la funcion (por ejemplo, "x**2 - 3").
        str_variable (str): Variable simbolica de la funcion (por ejemplo, "x").

    Returns:
        function: Funcion evaluable en Python usando la libreria math.

    Nota:
        Se usa sympy para convertir la expresion simbolica en una funcion evaluable.
    """ 
    x=sp.Symbol(str_variable)
    f_simbolic=sp.sympify(str_function)
    f_processed = sp.lambdify(x, f_simbolic, modules=["math"])
    return f_processed

def validate_function(str_func, str_var):  
    """
    Valida que una expresion matematica dada como string sea una funcion correcta
    y que la variable usada sea valida.

    Args:
        str_func (str): Expresion de la funcion.
        str_var (str): Variable esperada en la funcion.

    Returns:
        bool: True si la funcion es valida, False en caso contrario.

    Nota:
        Verifica que la variable exista en la expresion y que al evaluarla,
        retorne un valor numerico.
    """
    try:
        f=process_function(str_func,str_var)
        test=isinstance(f(1),(int,float))
        return (str_var in str_func and str_var.isalpha() and test)
    except (TypeError, ValueError):
        return False
    

def validate_nR_point0(enter_point):
    """
    Valida que el punto ingresado pueda ser convertido a numero flotante.

    Args:
        enter_point: Valor recibido (str, int, float).

    Returns:
        bool: True si el valor puede ser convertido a float, False si no.
    """
    try:
        return isinstance(float(enter_point),(int,float))
    except ValueError:
        return False
    



def graficar_nr(str_function, str_variable, a=None, b=None, results={}):
    """
    Grafica una funcion junto con las iteraciones del Metodo de Newton-Raphson.

    Args:
        str_function (str): Funcion como string.
        str_variable (str): Variable de la funcion.
        a (float, opcional): Limite inferior del eje x. Se ajusta automaticamente si no se da.
        b (float, opcional): Limite superior del eje x. Se ajusta automaticamente si no se da.
        results (dict): Diccionario con las aproximaciones por iteracion, generado por el metodo de Newton-Raphson.

    Detalles:
        - Muestra la curva de f(x) y las tangentes usadas en cada iteracion.
        - Representa graficamente los puntos generados durante el proceso.
        - Resalta la ultima aproximacion encontrada.
        - Ajusta automaticamente los ejes para mejorar la visualizacion.

    Requiere:
        matplotlib, numpy, sympy
    """
    xroots=[]
    x_center=0
    y_margin=1
    # Procesar función y derivada
    x=sp.Symbol(str_variable)
    f_sym=sp.sympify(str_function)  

    f=sp.lambdify(x, f_sym, modules=["numpy"])
    f_prime=sp.lambdify(x, sp.diff(f_sym, x), modules=["numpy"])

    # Obtener raíces estimadas desde el diccionario
    for head in results:
        if "root" in head:
            xroots=results[head]

    # Usar última raíz para centrar la gráfica
    if xroots:
        x_center=xroots[-1]

    # Rango automático si no se especifica a y b
    if a is None or b is None:
        a = x_center - 2
        b = x_center + 2

    x = np.linspace(a, b, 1000)
    y = f(x)

    # Ajuste automático del eje y para mejor visibilidad
    if np.max(y) - np.min(y) != 0:
        y_margin = (np.max(y) - np.min(y)) * 0.1

    y_min = np.min(y) - y_margin
    y_max = np.max(y) + y_margin

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label=f'$f({str_variable}) = {str_function}$')
    plt.axhline(0, color='black', linewidth=0.8)
    plt.axvline(0, color='black', linewidth=0.8)

    # Graficar las iteraciones de Newton-Raphson
    if results:
        for i in range(len(xroots)-1):
            x_k = float(xroots[i])
            fx_k = f(x_k)
            m = f_prime(x_k)
            if m == 0: continue  # evitar division por cero
            # Recta tangente: y = m*(x - x0) + f(x0)
            xtan = np.linspace(x_k - 100000, x_k + 100000, 10)
            ytan = m * (xtan - x_k) + fx_k
            plt.plot(xtan, ytan, '-', color='gray', linewidth=1) #se une xtan y ytan por medio de una linea, para representar la recta 

        if xroots:
            plt.scatter(xroots, [0]*len(xroots), color='red', label='Iteraciones') # puntos estimados
            plt.scatter([xroots[-1]], [0], color='blue', label='Aproximacion final') # ultima raiz
            plt.annotate(f'Raiz ≈ {xroots[-1]:.5f}', (xroots[-1], 0), textcoords="offset points", xytext=(0,10), ha='center', color='blue')

    plt.grid(True)
    plt.xlim(a, b)
    plt.ylim(y_min, y_max)
    plt.xlabel(f"${str_variable}$")
    plt.ylabel(f"$f({str_variable})$")
    plt.title("Gráfica de la función y método de Newton-Raphson")
    plt.legend()
    plt.tight_layout()
    plt.show()




