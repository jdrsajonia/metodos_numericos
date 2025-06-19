from regresion_lineal import LinealRegresion 
from regresion_lineal import getTabla
import time

def user_input():

    x_values=[]
    y_values=[]

    msg1="Calculadora de regresiones lineales de la forma AX + B\n"
    msg2="Ingrese los puntos para x:\n"
    ejemplo1="Ejemplo: \nX_k = 1 2 3 4 5\n"

    print(msg1)
    print(msg2)
    print(ejemplo1)
    while True:
        try:
            x_input=list(map(float, input(">> X_k = ").strip().split()))
            break
        except ValueError:
            print("ERROR: Los puntos son inválidos, intente nuevamente.\n")

    while True:
        print(f"\nIngrese {len(x_input)} para Y en total")
        try:
            y_input=list(map(float, input(">> Y_k = ").strip().split()))
            if len(y_input)!=len(x_input):
                raise ValueError("ERROR: La cantidad de puntos de Y es diferente de la de X")
            break
        except ValueError:
            print("ERROR: Los puntos son inválidos, intente nuevamente.\n")

    return x_input, y_input




def regresion_main(x_input=None, y_input=None, user_console=True):

    if user_console==True:
        x_input, y_input=user_input()

    recta=LinealRegresion(x_input,y_input)

    init=time.perf_counter()
    function=recta.get_function()
    end=time.perf_counter()
    print(f"Tiempo de ejecución: {end-init}")


    results=recta.get_table_values()
    print(getTabla(results, setTitle=f"f(x) = {function}", character=" "))
    recta.graphic_regresion()

    pass

regresion_main(user_console=True)