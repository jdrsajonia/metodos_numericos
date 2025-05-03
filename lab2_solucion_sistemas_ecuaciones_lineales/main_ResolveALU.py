import resolveALU as alu
import numpy as np

def main_ResolveALU():
    matriz = []
    title = "="*69 + "\nMétodo para resolver sistemas de ecuaciones lineales de la forma AX=B\n" + "="*69 + "\n"
    subtitle1 = "\nIngrese la dimensión de la matriz cuadrada A\nEj: Dimension = 3\n"
    subtitle2 = "\nIngrese los coeficientes de la matriz A por filas, separados por espacios\n(la matriz A debe ser cuadrada)\n\nEj:\nF1 = 2 9 1\nF2 = 5 3 7\nF3 = 8 1 0\n"
    subtitle3 = "\nIngrese los valores del vector B (términos independientes), separados por espacios\nEj: B = 1 2 3\n"

    print(title, subtitle1)
    dimension = int(input(">> Dimension = "))

    print(subtitle2)
    for i in range(dimension):
        fila = input(f">> F{i+1} = ")
        fila_valores = list(map(float, fila.strip().split()))
        if len(fila_valores) != dimension:
            raise ValueError(f"La fila {i+1} debe tener exactamente {dimension} elementos.")
        matriz.append(fila_valores)

    matriz_np = np.array(matriz)

    print(subtitle3)
    b_input = input(">> B = ")
    b_vector = list(map(float, b_input.strip().split()))
    if len(b_vector) != dimension:
        raise ValueError(f"El vector B debe tener exactamente {dimension} elementos.")

    b_np = np.array(b_vector)

    try:
        solucion = alu.resolve_AluMatrix(matriz_np, b_np)
        print("\nSolución del sistema AX = B:")
        for i, x in enumerate(solucion):
            print(f"x{i+1} = {x}")
    except Exception as e:
        print(f"\nError al resolver el sistema: {e}")

if __name__ == "__main__":
    main_ResolveALU()
