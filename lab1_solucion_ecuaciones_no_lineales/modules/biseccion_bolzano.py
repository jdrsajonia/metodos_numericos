import sympy as sp # instalar con pip install dado el caso
import matplotlib.pyplot as plt
import numpy as np

def bolzano(str_function,str_variable,a,b,tolerance=0.0001,decimal_notation=False):  
    """
    Implementa el metodo de Biseccion (Bolzano) para encontrar una raiz de la funcion f en el intervalo [a, b].

    Args:
        str_function (str): Funcion en formato string.
        str_variable (str): Variable de la funcion.
        a (float): Extremo izquierdo del intervalo.
        b (float): Extremo derecho del intervalo.
        tolerance (float): Tolerancia para detener la iteracion.
        decimal_notation (bool): Si es True, los resultados se formatean en notacion decimal.

    Returns:
        dict: Diccionario con los valores iterativos: k, a_k *root*, c_k, b_k y f(c_k).

    Nota:
        Se asume que f(a) y f(b) tienen signos opuestos.
    """
    results={"k":[],"a_k *root*":[],"c_k":[],"b_k":[],"f(c_k)":[],}
    
    def fmt(value): # # funcion interna que formatea los datos de results en decimales (opcional) 
        return f"{value:.8f}" if decimal_notation else value

    f = process_function(str_function,str_variable)
    k=0

    while k<200:
        c=(a+b)/2 #punto medio
        f_a = f(a)
        f_b = f(b)
        f_c = f(c) 

        results["k"].append(k)
        results["a_k *root*"].append(fmt(a))
        results["c_k"].append(fmt(c))
        results["b_k"].append(fmt(b))
        results["f(c_k)"].append(fmt(f_c))

        f_a_c = (f_a>0 and f_c<0) or (f_a<0 and f_c>0) # f(a) y f(c) tienen signos opuestos. Si es cierto, (a,c) --> (a,b)
        f_c_b = (f_b>0 and f_c<0) or (f_b<0 and f_c>0) # f(b) y f(c) tienen signos opuestos. Si es cierto, (b,c) --> (a,b)
        difference=abs(a-b)

        if (difference<=tolerance or f_c==0): # raiz exacta o sobrepaso de tolerancia
            break
        elif f_a_c: #decision de cual lado se recorta el intervalo, dado f(a), f(b) y f(c)
            b=c
        elif f_c_b:
            a=c
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


def validate_bolzano_interval(str_func,str_var,str_interval):
        """
        Valida si un intervalo [a, b] es adecuado para aplicar el Metodo de Biseccion (Bolzano),
        es decir, si f(a) y f(b) tienen signos opuestos.

        Args:
            str_func (str): Funcion en formato string.
            str_var (str): Variable de la funcion.
            str_interval (str): Intervalo como string separado por espacios, ej. "1 2".

        Returns:
            bool: True si el intervalo es valido, False si no lo es.

        Nota:
            Imprime un mensaje de error si f(a) y f(b) no tienen signos opuestos.
        """
        f=process_function(str_func,str_var)
        interval=str_interval.split()
        a=float(interval[0])
        b=float(interval[1])

        f_a=f(a)
        f_b=f(b)

        if f_a*f_b>0:
            print("\nError: f(a) y f(b) no tienen signos opuestos. \nf(a) = f({}) = {}\nf(b) = f({}) = {}\nVuelva a intentarlo\n".format(a,f_a,b,f_b))
            return False
        else:
            return True
   



def graficar_bb(str_function, str_variable, a=None, b=None, results={}, points=["a_k *root*","c_k","b_k"]):
    """
    Grafica una funcion junto con las iteraciones del Metodo de Biseccion (Bolzano).

    Args:
        str_function (str): Funcion como string.
        str_variable (str): Variable de la funcion.
        a (float, opcional): Limite inferior del eje x. Si no se da, se calcula automaticamente.
        b (float, opcional): Limite superior del eje x. Si no se da, se calcula automaticamente.
        results (dict): Diccionario de resultados generado por la funcion bolzano().
        points (list): Llaves de los puntos en el diccionario 'results' para graficar las iteraciones.

    Detalles:
        - Grafica f(x) en un rango adecuado.
        - Muestra los puntos de las iteraciones (a_k, c_k, b_k) en el eje x.
        - Resalta la ultima aproximacion con un punto rojo.
        - Añade etiquetas a los primeros y ultimos puntos evaluados.

    Requiere:
        matplotlib, numpy, sympy
    """
    # los nombres de las llaves del diccionario results, deben coincidir con la tabla que arroja el metodo de bolzano, tal como esta formateado en points
    if results: 
        a_kroots=results[points[0]]
        c_klist=results[points[1]]
        b_klist=results[points[2]]
    else:
        a_kroots=[]
        c_klist=[]
        b_klist=[]

    x_center=0
    y_margin=1

    # Procesar función
    x = sp.Symbol(str_variable)
    f_sym = sp.sympify(str_function)  
    f = sp.lambdify(x, f_sym, modules=["numpy"])

    # Usar última raíz para centrar la gráfica
    if a_kroots:
        x_center = a_kroots[-1]

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


    if results:
        y_range = np.max([f(a) for a in a_kroots] + [f(b) for b in b_klist] + [f(c) for c in c_klist])
        offset = y_range * 0.05  # Ajuste dinamico del desplazamiento de etiquetas
        # Etiquetar y graficar puntos según el caso
        for i in range(len(a_kroots)):
            f_a=f(a_kroots[i])
            f_c=f(c_klist[i])
            f_b=f(b_klist[i])

            f_a_c = (f_a > 0 and f_c < 0) or (f_a < 0 and f_c > 0)  # f(a) y f(c) tienen signos opuestos
            f_c_b = (f_b > 0 and f_c < 0) or (f_b < 0 and f_c > 0)  # f(b) y f(c) tienen signos opuestos 

            if f_a_c:
                plt.scatter(a_kroots[i], 0, color="green", label="Puntos A" if i == 0 else "")  # Etiqueta A
                plt.scatter(c_klist[i], 0, color="blue", label="Puntos B" if i == 0 else "")  # Etiqueta B
                if i==len(a_kroots)-1 or i==0:
                    # Etiqueta con texto para A y C
                    plt.text(a_kroots[i], offset, f"{i}", fontsize=9, ha="center", va="bottom", color="green")
                    plt.text(c_klist[i], offset, f"{i}", fontsize=9, ha="center", va="bottom", color="blue")
            elif f_c_b:
                plt.scatter(c_klist[i], 0, color="green", label="Puntos A" if i == 0 else "")  # Etiqueta C
                plt.scatter(b_klist[i], 0, color="blue", label="Puntos B" if i == 0 else "")  # Etiqueta B
                
                if i==len(a_kroots)-1 or i==0:
                    # Etiqueta con texto para B y C
                    plt.text(c_klist[i], offset, f"{i}", fontsize=9, ha="center", va="bottom", color="green")
                    plt.text(b_klist[i], offset, f"{i}", fontsize=9, ha="center", va="bottom", color="blue")
                
        plt.scatter([a_kroots[-1]], [0], color='red', label='Aproximacion final') # ultima raiz
        plt.annotate(f'Raiz ≈ {a_kroots[-1]:.5f}', (a_kroots[-1], 0), textcoords="offset points", xytext=(0,-15), ha='center', color='red') # ultima raiz

    plt.grid(True)
    plt.xlim(a, b)
    plt.ylim(y_min, y_max)
    plt.xlabel(f"${str_variable}$")
    plt.ylabel(f"$f({str_variable})$")
    plt.title("Gráfica de la función y método de Biseccion de Bolzano")
    plt.legend()
    plt.tight_layout()
    plt.show()



#añadir documentacion y cronometracion del codigo