import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import time 

def getTabla(heads_data,setTitle="",character=" "):
    '''

    Genera una tabla en formato de texto a partir de un diccionario de listas.

    Args:
        heads_data (dict): Llaves como encabezados y listas como columnas de datos.
        setTitle (str): Titulo de la tabla (opcional).
        character (str): Caracter de relleno para alinear texto (opcional).

    Returns:
        str: Representacion en string de la tabla formateada.

    Variables:
        table (str): Acumulador de texto para construir la tabla final.
        long_elements_x (dict): Guarda el ancho maximo necesario para cada columna.
        first_head (str): Primera llave del diccionario, usada para conocer el numero de filas.
        long_tabla_y (int): Altura de la tabla (numero de filas).
        long_tabla_x (int): Ancho total de la tabla (sumatoria de anchos de columnas).
        enmarcate (int): Ancho total de la tabla con bordes, usado para formatear y centrar.


    Nota:
        Todas las listas deben tener la misma longitud para evitar errores.


    '''
    table=""
    long_elements_x=dict()
    first_head=next(iter(heads_data))
    long_tabla_y=len(heads_data[first_head])


    if (long_tabla_y==0):
        return "Tabla sin datos"

    if len(character)>1: #si character son varios digitos, agarra el primero
        character=character[:1]

    for head in heads_data:
        # Este for consigue los mayores anchos necesarios para cada columna de la tabla, para mantener un formato
        long_element_x=max(map(str,heads_data[head]),key=len)
        long_head=len(head)
        long_data=len(long_element_x)
        long_elements_x[head]=max(long_head,long_data)

    long_tabla_x=sum(long_elements_x.values())
    enmarcate=long_tabla_x+2*len(heads_data)+len(heads_data)+1
    title=setTitle.center(enmarcate)

    table +="\n"+title+"\n"+"="*enmarcate+"\n"+"|"

    for head in heads_data:
        # Este for carga los encabezados del diccionario a la tabla
        tabulate=long_elements_x[head]
        text_head=str(head).center(tabulate,character)
        table+=" "+text_head+" |"

    table+="\n"+"="*enmarcate+"\n"

    for i in range(long_tabla_y):
        # Este for carga los datos obtenidos a la tabla
        table+="|"
        for head in heads_data:
            tabulate=long_elements_x[head]
            text_data=str(f"{heads_data[head][i]}").center(tabulate,character)
            table+=" "+text_data+" |"
        table+="\n"

    table+="="*enmarcate
    return table



def simplify_expresions(*polinomios):
    '''
    Simplifica las N expresiones algebráicas de SymPy pasadas como argumento

    Args:
        *polinomios: Conjunto de polinomios manejados con SymPy
    Returns:
        Lista de cada expresión simplificada
    '''
    simply_polinomiums=[]
    for polinomio in polinomios:
        simply_polinomiums.append(sp.simplify(polinomio))
    return simply_polinomiums




def lagrangeInterpolation(puntos_x_k:list, puntos_y_k:list, Ngrade:int):
    '''
    Aplica el método de Interpolación de Lagrange con los argumentos dados.

    Args:
        x_k (list): Lista con números de un conjunto de x.
        y_k (list): Lista con números de un conjunto de y.
        Ngrade (int): Grado de Interpolación.
    Returns:
        Polinomio algebráico de SymPy, en su forma extendida.
    '''

    if len(puntos_x_k)!=len(puntos_y_k):
        raise ValueError("Error: la cantidad de puntos de x, es diferente de la de y")
    polinomio=0
    x=sp.symbols('x') # variable algebraica

    # aplicación de la formula de Interpolación de Lagrange
    for k in range(Ngrade+1):
        termino=puntos_y_k[k]
        for j in range(Ngrade+1):
            if j!=k:
                L_k=(x-puntos_x_k[j])/(puntos_x_k[k]-puntos_x_k[j])
                termino=termino*L_k
        polinomio=polinomio+termino
    return polinomio



def calculate_ypoints(x_k:list,f:str):
    '''
    Calcula las imágenes de un conjunto de puntos X

    Args:
        x_k (list): Lista con el conjunto de puntos X
        f (str): Función escrita como String
    Returns:
        Lista de las imágenes de X dada la función f
    '''

    x=sp.symbols("x")
    return [sp.lambdify(x,f)(num) for num in x_k]



def lagrange_value_results(puntos_x_k:list,funcion:str,*polinomios):
    '''
    Crea un diccionario de valores para N polinomios, solamente si existe una función real f comparativa.

    Args:
        x_k (list): Lista con el conjunto de puntos de X usada para obtener un máximo y mínimo en el dominio.
        f (str): Función algebráica pasada como String
        polinomios: N cantidad de polinomios de SymPy  
    Returns:
        Diccionario con la función real f, los polinomios P_n y sus errores y un dominio de X entre min(x_k) y max(x_k)

    '''
    if not isinstance(funcion,str):
        print("\nTabla de resultados no disponible para valores discretos de Y. Se necesita una función algebráica como texto String.\n")
        return

    results={}
    
    puntos_x=np.linspace(min(puntos_x_k),max(puntos_x_k),13) # generación del dominio de x
    results["x_k"]=np.round(puntos_x,1)
    results[f"f(x) = {funcion}"]=calculate_ypoints(puntos_x,funcion)

    # almacenamiento de valores calculados en x para la función real, los N polinomios y sus errores 
    for i,polinomio in enumerate(polinomios):
        results[f"P_{i}(x)"]=calculate_ypoints(puntos_x,polinomio)
        if len(polinomios)!=1:
            results[f"f(x) - P_{i}(x)"] = np.subtract(calculate_ypoints(puntos_x,funcion),calculate_ypoints(puntos_x,polinomio)) # errores
    return results



def graficar_lagrange(puntos_x_k:list, funcion:str, *polinomios):
    """
    Grafica uno o más polinomios de interpolación junto a la función original (opcional).

    Args:
    - puntos_x_k: lista de nodos (valores de x).
    - funcion: expresión en string de la función original f(x), o una cadena vacía si no se desea graficar.
    - *polinomios: uno o más polinomios simbólicos de interpolación (tipo sympy).

    
    Grafica cada polinomio en su propio subplot.
    Si se proporciona una función válida, la grafica como línea discontinua.
    Resalta los puntos nodales en cada gráfico.
    """
    
    x=sp.symbols("x")
    num_polinomios=len(polinomios)

    x_dominio=np.linspace(min(puntos_x_k), max(puntos_x_k), 500)

    es_funcion=isinstance(funcion, str)
    if es_funcion:
        try:
            funcion_expresion=sp.sympify(funcion)
            funcion_lambd=sp.lambdify(x, funcion_expresion)
            valores_y=[funcion_lambd(val) for val in x_dominio]
        except:
            es_funcion = False

    cols=2
    rows=int(np.ceil(num_polinomios / cols))
    fig, axes=plt.subplots(rows, cols, figsize=(10, 4 * rows))
    axes=axes.flatten()

    for i, pol in enumerate(polinomios):
        ax=axes[i]
        pol_lambd=sp.lambdify(x, pol)
        y_pol=[pol_lambd(val) for val in x_dominio]

        if es_funcion:
            ax.plot(x_dominio, valores_y, label=f"f(x) = {funcion}", linestyle="--", color="black")
        ax.plot(x_dominio, y_pol, label=f"P_{i}(x)", color="blue")

        # puntos nodales
        ax.scatter(puntos_x_k, [pol_lambd(xi) for xi in puntos_x_k], color='red', zorder=5, label="Puntos nodales")

        # estética
        ax.set_title(f"P_{i}(x)")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        ax.axhline(0, color='black', linewidth=1.1, linestyle='-')
        ax.axvline(0, color='black', linewidth=1.1, linestyle='-')
        ax.legend()

    # easliminar ejes vacíos
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()






def user_input():
    titulo="="*25+"\nInterpolación de Lagrange\n"+"="*25
    msg1="Cuenta con una función f(x)? \nNo: [0]\nSi: [1]"
    msg2="\nIngrese una función algebráica simbólica\nEj: f(x) = 2*x**3+1"
    msg3="\nIngrese el grado del polinomio interpolador "
    msg4="\nCuantos polinomios interpolados quieres generar?"
    msg5=f"\nIngrese los puntos nodos de X  (y Y si es el caso), separados por espacios\nEj:\nX_k = 1.2 3.2 4.0 7\nY_k= 7 9 12"

    xvalues=[]
    yvalues=[]

    print(titulo)
    print(msg1)
    while True:
        try:
            response=int(input(">> "))
            if response==0 or response==1:
                break
            else:
                raise ValueError
        except ValueError:
            print("ERROR: Respuesta inválida, debe ser 0 para NO o 1 para SI")

    if response==1:
        print(msg2)
        while True:
            try: 
                yvalues=input(">> f(x) = ")
                
                f=sp.lambdify(sp.symbols("x"),yvalues)
                test=f(1234)
                
                break
            except Exception:
                print("ERROR: La función es inválida, intente de nuevo.")


    print(msg3)
    while True:
        try:
            grado = int(input(">> N = "))
            if grado<=0:
                raise ValueError()
            break
        except ValueError:
            print("ERROR: el grado es inválido")

    warning=f"RECUERDA: Tienes que ingresar {grado+1} puntos:"

    print(msg4)
    while True:
        try:
            num_polinomios = int(input(">> "))
            if num_polinomios <= 0:
                raise ValueError()
            break
        except ValueError:
            print("ERROR: el número debe ser un entero positivo.")

    print(msg5)
    print(warning)
    for i in range(num_polinomios):
        print(f"\nPuntos (x,y) para P_{i+1}")
        
        while True:
            try:
                
                entradax=list(map(float, input(">> X_k = ").strip().split()))
                if response==0:
                    entraday=list(map(float, input(">> Y_k = ").strip().split()))
                    if len(entraday)!=grado+1:
                        raise ValueError
                    yvalues.append(entraday) 
                    

                if len(entradax)!=grado+1:
                    raise ValueError
                xvalues.append(entradax)
                break
            except ValueError:
                print("ERROR: Los puntos son inválidos, intente nuevamente.")
    print()
    return xvalues, yvalues, grado



def main(xvalues=None,function=None,grade=None,user_console=False):
    if user_console:
        xvalues, function, grade = user_input()

    polinomios = []
    es_funcion = isinstance(function, str)
    y_listas = []
    if es_funcion:
        for xlist in xvalues:
            y_listas.append(calculate_ypoints(xlist, function))
    else:
        y_listas = function  # ya son listas numéricas

    # se crean los polinomios para cada conjunto
    for xlist, ylist in zip(xvalues, y_listas):
        init=time.perf_counter()
        polinomios.append(lagrangeInterpolation(xlist, ylist, grade))
        end=time.perf_counter()
        print(f"Tiempo de ejecución: {end-init}")

    results=lagrange_value_results(xvalues[0], function, *polinomios)
    expresiones_simplificadas=simplify_expresions(*polinomios)

    for i,simply_expresion in enumerate(expresiones_simplificadas):
        print(f"P_{i}(x) = {simply_expresion}")

    if es_funcion:
        print(getTabla(results, " "))

    graficar_lagrange(xvalues[0],function, *expresiones_simplificadas)


main(user_console=True)