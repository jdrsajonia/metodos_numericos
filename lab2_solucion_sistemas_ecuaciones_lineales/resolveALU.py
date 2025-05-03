import numpy as np

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


def sustitucionRegresiva(matrix,independent):
    """
    Resuelve un sistema de ecuaciones lineales con matriz triangular superior mediante sustitución regresiva.

    Args:
        matrix (np.ndarray): Matriz triangular superior de coeficientes (forma n x n).
        independent (np.ndarray): Vector columna de términos independientes (forma n,).

    Returns:
        list: Lista con la solución del sistema (forma n,).
    """
    is_uptriangular=np.allclose(matrix, np.triu(matrix))

    if not is_uptriangular: # verifica que la matriz sea triangular superior
        raise ValueError("La matriz no es triangular superior")
    
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
    is_lowtriangular=np.allclose(matrix, np.tril(matrix))

    if not is_lowtriangular: # verifica que la matriz sea triangular inferior
        raise ValueError("La matriz no es triangular inferior")
    
    n_dim=matrix.shape[0]
    solutions=[0.0]*n_dim # no se usa insert para mejorar eficiencia. Usaremos acceso directo a memoria
    xn=independent[0]/matrix[0,0]
    solutions[0]=xn

    for i in range(1,n_dim): #se recorre desde 1 hasta n
        x_i=(independent[i]-(np.dot(matrix[i,:i],solutions[:i])))/matrix[i,i]
        solutions[i]=x_i
    return solutions
    

def factorizacionLU(matrix):
    """
    Realiza la factorización LU sin pivoteo de una matriz cuadrada A.

    Args:
        matrix (np.ndarray): Matriz cuadrada.

    Returns:
        tuple: (L, U) donde A = LU.

    Raises:
        ValueError: Si se detecta un pivote cero (requiere pivoteo).
        TypeError: Si la matriz no es un objeto np.ndarray.
        bool: Retorna False si la matriz no es cuadrada o no tiene solución única.
    """ 
    if not has_unique_solutions(matrix):
        raise ValueError("La matriz ingresada no es válida (debe tener única solución)")
    
    U_matrix=matrix.copy()
    n_dim=U_matrix.shape[0] # dimension filas
    L_matrix=np.eye(n_dim)
    
    for j in range(0,n_dim):
        for i in range(j+1,n_dim):

            if np.isclose(U_matrix[j, j], 0):
                raise ValueError(f"Pivote cero detectado en fila {j}. Requiere pivoteo.\n{U_matrix}")
            
            m_ij=U_matrix[i,j]/U_matrix[j,j] # multiplicador 
            U_matrix[i]=U_matrix[i]-m_ij*U_matrix[j] # se opera la fila de la matriz actual con la fila j
            L_matrix[i,j]=m_ij # se guarda el multiplicador en L
            
    return L_matrix, U_matrix



def resolve_AluMatrix(matrix, independent):
    """
    Resuelve el sistema AX = B usando factorización LU sin pivoteo (directa).

    Args:
        matrix (np.ndarray): Matriz de coeficientes A NxN.
        independent (np.ndarray): Vector columna B 1xN.

    Returns:
        np.ndarray: Solución X del sistema AX = B.
    """

    L_matrix, U_matrix = factorizacionLU(matrix)
    y_vector=sustitucionProgresiva(L_matrix,independent) # LY=B
    x_vector=sustitucionRegresiva(U_matrix,y_vector) # UX = Y
    
    return x_vector




