import math
import numpy as np
import time
import sys

class Iteration:
    '''
    documentar aqui
    '''
    count = 0
    iterations = []
    Q = []
    # Constructor:
    def __init__(self, P):
        Iteration.iterations.append(self)
        self.id = Iteration.count
        self.P = P
        self.convergence = self.euclideanDistance()
        Iteration.count += 1

    def euclideanDistance(self):
        return math.sqrt(sum((pi - qi) ** 2 for pi, qi in zip(self.P, Iteration.Q))) # Calcula la distancia euclidea a vector solucion Q.

    # Método de impresión.
    def __str__(self):
        valores = '\t'.join(f"{x:.6f}" for x in self.P)  # 6 decimales, ajustar
        return f"{self.id}\t\t{valores} \t{self.convergence:.6e}"

    @staticmethod
    def last():
        return Iteration.iterations[-1]

    @staticmethod
    def setQ(Q):
        Iteration.Q = Q
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
            text_data=str(heads_data[head][i]).center(tabulate,character)
            table+=" "+text_data+" |"
        table+="\n"

    table+="="*enmarcate
    return table
def isStrictlyDominant(M):
    '''
    Documentar aqui
    '''
    for i in range(len(M)):
        diag = abs(M[i][i])
        suma = sum(abs(M[i][j]) for j in range(len(M)) if j != i)
        if diag <= suma:
            print(f"\nLa fila {i} no cumple criterio de Estrictamente dominante: |{M[i][i]}| <= {suma}")
            return False
    print(f"\nLa matriz ingresada es estrictamente dominante.")
    return True


def has_unique_solutions(matrix):
    """
    Verifica si una matriz cuadrada tiene solución única para el sistema Ax = B.

    Args:
        matrix (np.ndarray): Matriz de coeficientes (forma n x n).

    Returns:
        bool: True si la matriz es cuadrada e invertible (det ≠ 0), False en caso contrario.
    """

    if not isinstance(matrix, np.ndarray):
        raise TypeError("Matriz mal escrita - (necesita ser un objeto np.ndarray)")

    is_square=matrix.shape[0]==matrix.shape[1]
    if not is_square:
        return False
    if np.isclose(np.linalg.det(matrix),0):
        return False
    return True

def jacobiMethod(M, B, P0, t):
    '''
    Documentar aqui
    '''
    # Comienzo de iteraciones.
    # Iteración inicial.
    Iteration(P0)

    # Otras iteraciones.
    n = 0
    while n < 100:
        P = []
        for i in range(M.shape[0]):       # filas
            sum = 0
            for j in range(M.shape[1]):   # columnas
                if i != j:
                    sum += M[i][j] * Iteration.last().P[j]
                if i == j:
                    a = M[i][j]

            xi = (B[i] - sum) / a
            P.append(float(xi))
        # Se guarda la iteración.
        Iteration(P)
        if Iteration.last().convergence < t:
            break
        n += 1
        
def user_input():
    title="="*69 + "\nMétodo para resolver sistemas de ecuaciones lineales de la forma AX=B\n" + "="*69 + "\n"
    subtitle1="\nIngrese la dimensión de la matriz cuadrada A\nEj: Dimension = 3\n"
    subtitle2="\nIngrese los coeficientes de la matriz A por filas, separados por espacios\n(la matriz A debe ser cuadrada)\n\nEj:\nF1 = 2 9 1\nF2 = 5 3 7\nF3 = 8 1 0\n"
    subtitle3="\nIngrese los valores del vector B (términos independientes), separados por espacios\nEj: B = 1 2 3\n"

    print(title, subtitle1)

    while True:
        try:
            dimension=int(input(">> Dimension = "))
            if dimension <= 0:
                raise ValueError("La dimensión debe ser un entero positivo.")
            break
        except ValueError:
            print("Entrada inválida. Ingrese un número entero positivo.\n")

    print(subtitle2)

    while True:
        matriz=[]
        try:
            for i in range(dimension):
                fila = input(f">> F{i+1} = ")
                fila_valores = list(map(float, fila.strip().split()))
                if len(fila_valores) != dimension:
                    raise ValueError()
                matriz.append(fila_valores)

            matriz_np = np.array(matriz)

            if has_unique_solutions(matriz_np):
                break
            else:
                print("Esta matriz no tiene solución única. Intente con otra.\n")
        except ValueError:
            print(f"Error: Cada fila debe tener exactamente {dimension} números válidos.\n")
        except Exception as e:
            print(f"Error inesperado: {e}\n")

    print(subtitle3)

    while True:
        try:
            b_input = input(">> B = ")
            b_vector = list(map(float, b_input.strip().split()))
            if len(b_vector) != dimension:
                raise ValueError()
            b_np = np.array(b_vector)
            break
        except ValueError:
            print(f" El vector B debe tener exactamente {dimension} elementos numéricos. Intente de nuevo.\n")

    return matriz_np, b_np

def obtenerResultados():
    results = {
        "k": [],
        "distancia": []
    }

    if not Iteration.iterations:
        return results

    n = len(Iteration.iterations[0].P)  # número de variables

    # Crear claves dinámicamente: x1, x2, ..., xn
    for i in range(n):
        results[f"x{i+1}"] = []

    # Llenar el diccionario
    for iteracion in Iteration.iterations:
        results["k"].append(iteracion.id)
        results["distancia"].append(iteracion.convergence)
        for i in range(n):
            results[f"x{i+1}"].append(iteracion.P[i])

    return results

# Start main.
def run():
    # Inicializa la matriz M y B.
    M, B = user_input()
    # Muestra la matriz M y el vector B ingresados.
    print("-" * 80)
    print(f"\nLa matriz ingresada es:\n{M}\nEl vector de coeficientes es: \n{B}")
    # Verificación de si es estrictamente dominante.
    if not isStrictlyDominant(M):
        sys.exit(0)

    print("-" * 80)
    # Entrada de la tolerancia deseada.
    t = float(input("\nIngrese la tolerancia deseada: "))

    # Entrada del vector inicial.
    initialSol = input("\nIngrese la solución inicial (separada por espacios): ")
    P0 = np.array([float(x) for x in initialSol.split()])

    # Solución exacta.
    exactSol = input("\nIngrese la solución exacta (separada por espacios): ")
    Q = np.array([float(x) for x in exactSol.split()])
    Iteration.setQ(Q)

    # Llevar a cabo el metodo con las condiciones dadas.
    init=time.perf_counter()
    jacobiMethod(M, B, P0, t)
    end=time.perf_counter()

    # Imprimir resultados -----------------------------------------------------
    
    results=obtenerResultados()
    # Imprimir encabezados.
    print(getTabla(results,setTitle="Metodo de Jacobi"))
    print(f"Tiempo de ejecución {end-init}")

run()