import numpy as np

def sustitucionRegresiva(matrix,independent):
    """
    Resuelve un sistema de ecuaciones lineales con matriz triangular superior mediante sustitución regresiva.

    Args:
        matrix (np.ndarray): Matriz triangular superior de coeficientes (forma n x n).
        independent (np.ndarray): Vector columna de términos independientes (forma n,).

    Returns:
        list: Lista con la solución del sistema (forma n,).
    """
    n_dim=matrix.shape[0] 
    solutions=[0.0]*n_dim #no se usa insert para mejorar eficiencia. Usaremos acceso directo a memoria

    xn=independent[-1]/matrix[-1,-1]
    solutions[-1]=xn

    for i in range(n_dim-2,-1,-1): #se recorre desde n-1 hasta 0 (recordar que empieza con indice cero, por eso n_dim-2 --> ndim-1-1)
        x_i=(independent[i]-(np.dot(matrix[i,i+1:],solutions[i+1:])))/matrix[i,i]
        solutions[i]=x_i
    return solutions


def sustitucionProgresiva(matrix, independent):
    """
    Resuelve un sistema de ecuaciones lineales con matriz triangular inferior mediante sustitución progresiva.

    Args:
        matrix (np.ndarray): Matriz triangular inferior de coeficientes (forma n x n).
        independent (np.ndarray): Vector columna de términos independientes (forma n,).

    Returns:
        list: Lista con la solución del sistema (forma n,).
    """
    n_dim=matrix.shape[0]
    solutions=[0.0]*n_dim #no se usa insert para mejorar eficiencia. Usaremos acceso directo a memoria

    xn=independent[0]/matrix[0,0]
    solutions[0]=xn

    for i in range(1,n_dim): #se recorre desde 1 hasta n
        x_i=(independent[i]-(np.dot(matrix[i,:i],solutions[:i])))/matrix[i,i]
        solutions[i]=x_i
    return solutions
    


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
    if np.linalg.det(matrix)==0:
        return False
    return True


def is_triangular(matrix):
    """
    Determina si una matriz es triangular (superior o inferior).

    Args:
        matrix (np.ndarray): Matriz a evaluar (forma n x n).

    Returns:
        bool: True si es triangular (superior o inferior), False en caso contrario.
    """
    return is_uptriangular(matrix) or is_lowtriangular(matrix)


def is_uptriangular(matrix):
    """
    Verifica si una matriz es triangular superior.

    Args:
        matrix (np.ndarray): Matriz a evaluar (forma n x n).

    Returns:
        bool: True si todos los elementos por debajo de la diagonal son cero.
    """
    return np.allclose(matrix, np.triu(matrix))


def is_lowtriangular(matrix):
    """
    Verifica si una matriz es triangular inferior.
    
    Args:
        matrix (np.ndarray): Matriz a evaluar (forma n x n).

    Returns:
        bool: True si todos los elementos por encima de la diagonal son cero.
    """
    return np.allclose(matrix, np.tril(matrix))


