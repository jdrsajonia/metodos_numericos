import lagrange as lg
import numpy as np
import time 
import sympy as sp
import matplotlib.pyplot as plt
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
            y_listas.append(lg.calculate_ypoints(xlist, function))
    else:
        y_listas = function  # ya son listas numéricas

    # se crean los polinomios para cada conjunto
    for xlist, ylist in zip(xvalues, y_listas):
        init=time.perf_counter()
        polinomios.append(lg.lagrangeInterpolation(xlist, ylist, grade))
        end=time.perf_counter()
        print(f"Tiempo de ejecución: {end-init}")

    results=lg.lagrange_value_results(xvalues[0], function, *polinomios)
    expresiones_simplificadas=lg.simplify_expresions(*polinomios)

    for i,simply_expresion in enumerate(expresiones_simplificadas):
        print(f"P_{i}(x) = {simply_expresion}")

    if es_funcion:
        print(lg.getTabla(results, " "))

    lg.graficar_lagrange(xvalues[0],function, *expresiones_simplificadas)


main(user_console=True)