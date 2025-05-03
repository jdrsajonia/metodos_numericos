import numpy as np
import resolveALU as alu

# MATRICES GENERALES NO TRIANGULARES
general = [
    np.array([[2, 1],
              [3, 4]]),  # 2x2

    np.array([[0, 2, 1],
              [1, -1, 0],
              [3, 2, 5]]),  # 3x3

    np.array([[4, 2, 3, 1],
              [1, 1, 1, 1],
              [3, 5, 2, 0],
              [2, 4, 1, 3]]),  # 4x4

    np.array([[1, 2, 3, 4, 5],
              [5, 4, 3, 2, 1],
              [2, 3, 4, 5, 6],
              [6, 5, 4, 3, 2],
              [1, 3, 5, 7, 9]]),  # 5x5

    np.array([[1, 0, 2, -1, 3, 4],
              [2, 1, 0, 3, -2, 5],
              [0, 1, 2, 1, 0, 1],
              [3, -2, 1, 4, 1, 2],
              [4, 2, 1, 0, 3, 1],
              [1, 3, 2, 1, 2, 4]]),  # 6x6
]

# COLUMNAS DE TÉRMINOS INDEPENDIENTES CORRESPONDIENTES
C = [
    np.array([5, 6]),

    np.array([4, 1, 10]),

    np.array([20, 10, 15, 30]),

    np.array([15, 25, 35, 45, 55]),

    np.array([7, 8, 9, 10, 11, 12])
]


for matrix, independent in zip(general, C):
    try:
        print(alu.resolve_AluMatrix(matrix, independent))
    except ValueError:
        print(f"Error en la matriz:\n {matrix}")


A=np.array([[4, 2, 3, 1],
              [1, 1, 1, 1],
              [3, 5, 2, 0],
              [2, 4, 1, 3]])

B=np.array([[21],
            [52],
            [79],
            [82]])

amp_AB=np.array([[1,2,4,1,21],
                 [2,8,6,4,52],
                 [3,10,8,8,79],
                 [4,12,10,6,82]])



#l,u = su.factorizacionLU(A)

#print(l)
#print(u)



#print(su.resolve_AluMatrix(A,B))


# MATRICES SINGULARES (NO INVERTIBLES)
singulares = [
    np.array([[1, 2],
              [2, 4]]),  # filas linealmente dependientes

    np.array([[0, 1, 2],
              [1, 2, 3],
              [2, 4, 6]]),  # filas linealmente dependientes

    np.array([[3, 6, 9, 12],
              [1, 2, 3, 4],
              [2, 4, 6, 8],
              [5, 10, 15, 20]])  # combinación lineal de filas
]

# COLUMNAS CORRESPONDIENTES (pueden causar inconsistencias)
C_singulares = [
    np.array([5, 10]),

    np.array([1, 2, 3]),

    np.array([6, 2, 4, 10])
]

for matrix, independent in zip(singulares, C_singulares):

    print(alu.resolve_AluMatrix(matrix, independent))
 
