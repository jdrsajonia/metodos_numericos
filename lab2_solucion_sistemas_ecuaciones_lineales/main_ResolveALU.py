import resolveALU as alu
import numpy as np
import time 


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

            if alu.has_unique_solutions(matriz_np):
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


def ALUmain(matrix=[], independent=[], console_input=False):
    if console_input:
        matrix, independent = user_input()
    try:
        init=time.perf_counter()
        solucion = alu.resolve_AluMatrix(matrix, independent)
        end=time.perf_counter()
        print("\nSolución del sistema AX = B:")
        for i, x in enumerate(solucion):
            print(f"x{i+1} = {x}")
    except Exception as e:
        print(f"\nError al resolver el sistema: {e}")

    print(f"Tiempo de ejecución: {end-init}")
    alu.graphic_system(matrix,independent,solucion)


ALUmain(console_input=True)