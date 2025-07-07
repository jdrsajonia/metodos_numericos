import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  

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
    
    
    U_matrix=matrix.astype(float).copy()
    n_dim=U_matrix.shape[0]
    L_matrix=np.eye(n_dim, dtype=float)
    
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





def graphic_system(matrix,independent,x_vector):
    """
    Grafica sistemas de ecuaciones lineales con solución única para dimensiones 2x2 o 3x3.

    Args:
        matrix (np.ndarray): Matriz de coeficientes A (2x2 o 3x3).
        independent (np.ndarray): Vector de términos independientes B.
        x_vector (list or np.ndarray): Solución del sistema AX = B.

    Nota:
        - En 2D grafica rectas.
        - En 3D grafica planos.
        - Muestra el punto de intersección si existe.
    """
    dimension=matrix.shape[0]
    
    if dimension==2: 
        plt.figure(figsize=(12, 8)) 
        x=np.linspace(x_vector[0]-100,x_vector[0]+100,400)

        for i in range(2):
            a1=matrix[i,0]
            a2=matrix[i,1]
            b=independent[i]

            if np.isclose(a2,0): # si la recta es vertical
                y=np.full_like(x,np.nan)
                x_vertical=b/a1
                plt.axvline(x_vertical,color='green')
            else:
                y=(b-a1*x)/a2 # se obtienen todas las imagenes para todas las rectas
            plt.plot(x,y, label=f"Ec{i+1}: {a1}*x + ({a2})*y = {b}") # se dibuja la recta 

        if x_vector: # se dibuja el punto solución si se pasa como argumento
            plt.scatter(x_vector[0],x_vector[1],color="red",label=f"Punto de corte: ({x_vector[0]:.1f},{x_vector[1]:.1f})" ) 

        # se ajustan detalles de la grafica   
        plt.axhline(0,color='black',linewidth=1)
        plt.axvline(0,color='black',linewidth=1)
        plt.grid(True)
        plt.legend()
        plt.xlabel("x")
        plt.ylabel("y")
        plt.tight_layout()
        plt.show()

    elif dimension == 3:
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        for i in range(3):
            a, b, c = matrix[i]
            d = independent[i]

            if np.isclose(c, 0):  # plano vertical (no depende de z)
                x_vals = np.linspace(x_vector[0] - 10, x_vector[0] + 10, 30)
                z_vals = np.linspace(x_vector[2] - 10, x_vector[2] + 10, 30)
                X, Z = np.meshgrid(x_vals, z_vals)
                if not np.isclose(b, 0):  # evitar división por cero
                    Y = (d - a * X) / b
                    ax.plot_surface(X, Y, Z, alpha=0.5, label=f"Ecuación {i+1}", cmap='viridis')
                else:
                    print(f"No se puede graficar el plano {i+1}: a={a}, b={b}, c={c}")
            else:
                x_vals = np.linspace(x_vector[0] - 10, x_vector[0] + 10, 30) # depende de z
                y_vals = np.linspace(x_vector[1] - 10, x_vector[1] + 10, 30)
                X, Y = np.meshgrid(x_vals, y_vals)
                Z = (d - a * X - b * Y) / c
                ax.plot_surface(X, Y, Z, alpha=0.5, label=f"Ec{i+1}: {a}*x + ({b})*y + ({c}) = {d}", cmap='viridis')

        if x_vector: # se dibuja el punto solución si se pasa como argumento
            ax.scatter(*x_vector, color='red', label=f'Solución ({x_vector[0]:.1f}, {x_vector[1]:.1f}, {x_vector[2]:.1f})')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('Sistema de Ecuaciones Lineales (3x3)')
        ax.grid(True)
        plt.legend()
        plt.show()

    else:
        print("solo disponible para dimension 2 o 3")

    


