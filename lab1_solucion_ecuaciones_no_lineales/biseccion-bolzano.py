import generate_table as table
from math import *

def bolzano(function,a,b, tolerance=0.0001):  
    results={"k":[],"a_k":[],"c_k":[],"b_k":[],"f(c_k)":[],}
    f = lambda x:eval(function)
    k=0

    while True:
        c=(a+b)/2 #punto medio
        f_a = f(a)
        f_b = f(b)
        f_c = f(c) 

        results["k"].append(k)
        results["a_k"].append(a)
        results["c_k"].append(c)
        results["b_k"].append(b)
        results["f(c_k)"].append(f_c)

        f_a_c = (f_a>0 and f_c<0) or (f_a<0 and f_c>0) # f(a) y f(c) tienen signos opuestos. Si es cierto, (a,c) --> (a,b)
        f_c_b = (f_b>0 and f_c<0) or (f_b<0 and f_c>0) # f(b) y f(c) tienen signos opuestos. Si es cierto, (a,c) --> (a,b)
        difference=abs(a-b)

        if (difference<=tolerance or f_c==0): # raiz exacta o sobrepaso de tolerancia
            break
        elif f_a_c:
            b=c
        elif f_c_b:
            a=c
        k=k+1
    return results



def insert_function():

    while True:
        try:
            enter_funcion=input("\nIngresa una funcion en terminos de x, correctamente escrita en sintaxis de Python (usar 'math' si es necesario)\n---> f(x) = ")
            f = lambda x: eval(enter_funcion)
            resultado = f(1)
            return enter_funcion, f   
        except Exception as e:
            print(f"Función inválida: {e}")
            print("Por favor, intenta nuevamente.\n")


def insert_interval(f):
    
    while True:
        enter_interval=input("\nIngresa un intervalo a, b donde f(a) y f(b) tienen signos opuestos siguiendo el formato 'a b'\n---> a b : ")

        interval=list(map(float,enter_interval.split()))
        a=interval[0]
        b=interval[1]

        f_a=f(a)
        f_b=f(b)

        if f_a*f_b>0:
            print("\nError: f(a) y f(b) no tienen signos opuestos. \nf(a) = f({}) = {}\nf(b) = f({}) = {}\nVuelva a intentarlo\n".format(a,f_a,b,f_b))
        else:
            return a,b



str_funcion, function=insert_function()
a, b = insert_interval(function)

resultados=bolzano(str_funcion,a,b)
titulo="Biseccion de Bolzano para f(x) = {}".format(str_funcion)

print(table.getTabla(resultados,setTitle=titulo))

