import generate_table as table
import sympy as sp #instalar con pip install
import time


def process_function(str_function, str_variable):
    x=sp.Symbol(str_variable)
    f_simbolic=sp.sympify(str_function)
    f_processed = sp.lambdify(x, f_simbolic, modules=["math"])
    return f_processed


def bolzano(str_function,str_variable,a,b,tolerance=0.0001,decimal_notation=False):  
    results={"k":[],"a_k *root*":[],"c_k":[],"b_k":[],"f(c_k)":[],}
    #funcion interna para formatear en decimal a los datos
    def fmt(value): 
        return f"{value:.8f}" if decimal_notation else value

    f = process_function(str_function,str_variable)
    k=0

    while k<200:
        c=(a+b)/2 #punto medio
        f_a = f(a)
        f_b = f(b)
        f_c = f(c) 

        results["k"].append(k)
        results["a_k *root*"].append(fmt(a))
        results["c_k"].append(fmt(c))
        results["b_k"].append(fmt(b))
        results["f(c_k)"].append(fmt(f_c))

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


def validate_function(str_func, str_var):  
    try:
        f=process_function(str_func,str_var)
        test=isinstance(f(1),(int,float))
        return (str_var in str_func and str_var.isalpha() and test)
    except (TypeError, ValueError):
        return False


def validate_bolzano_interval(str_func,str_var,str_interval):

        f=process_function(str_func,str_var)
        interval=str_interval.split()
        a=float(interval[0])
        b=float(interval[1])

        f_a=f(a)
        f_b=f(b)

        if f_a*f_b>0:
            print("\nError: f(a) y f(b) no tienen signos opuestos. \nf(a) = f({}) = {}\nf(b) = f({}) = {}\nVuelva a intentarlo\n".format(a,f_a,b,f_b))
            return False
        else:
            return True
   


# flujo del programa:
def bolzano_main():
    var=input("var: ")
    func=input("func: ")

    while not validate_function(func,var):
        var=input("var again: ")
        func=input("func again: ")

    interval=input("interval: ")
    while not validate_bolzano_interval(func,var,interval):
        interval=input("interval again: ")

    interval=interval.split()
    a=float(interval[0])
    b=float(interval[1])


    init=time.time()
    result=bolzano(func,var,a,b)
    end=time.time()

    duracion=end-init

    titulo="Biseccion de Bolzano para f(x) = {}".format(func)
    tabla=table.getTabla(result,setTitle=titulo)
    print(tabla)
    print(f"Tiempo de ejecucion: {duracion:.8f}")

bolzano_main()



#añadir documentacion y cronometracion del codigo