import generate_table as table
import sympy as sp #instalar con pip install
import time



def process_function(str_function, str_variable): #validar funcion en esta misma
    x=sp.Symbol(str_variable)
    f_simbolic=sp.sympify(str_function)
    f_processed = sp.lambdify(x, f_simbolic, modules=["math"])
    return f_processed


def newtonRapshon(str_function, variable, point_k0, tolerance=0.0001, decimal_notation=False):
    results={"k":[],"P_k *root*":[],"(P_k+1)-(P_k)":[],"f(P_k)":[]}

    def fmt(value):
        return f"{value:.8f}" if decimal_notation else value
    
    x = sp.Symbol(variable)
    # funciones simbolicas
    f_simbolic = sp.sympify(str_function) 
    f_diff_simbolic = sp.diff(f_simbolic, x) 

    # lambdify vuelve las funciones simbolicas en expresiones evaluables para Python
    f = sp.lambdify(x, f_simbolic, modules=["math"]) # f(x)
    f_diff = sp.lambdify(x, f_diff_simbolic, modules=["math"]) # f´(x) 
    k=0

    while True:
        f_pk=f(point_k0) # f(pk)
        f_diff_pk=f_diff(point_k0) # f´(pk)

        if f_diff_pk==0:
            results["k"].append(k)
            results["P_k *root*"].append(fmt(point_k0))
            results["(P_k+1)-(P_k)"].append("None")
            results["f(P_k)"].append(fmt(f_pk))
            break

        point_k1=point_k0-(f_pk/f_diff_pk)
        difference=abs(point_k1-point_k0)

        results["k"].append(k)
        results["P_k *root*"].append(fmt(point_k0))
        results["(P_k+1)-(P_k)"].append(fmt(difference))
        results["f(P_k)"].append(fmt(f_pk))
        point_k0=point_k1
        
        if difference<tolerance:
            break
        k=k+1
    return results
    

def validate_function(str_func, str_var):  
    try:
        f=process_function(str_func,str_var)
        test=isinstance(f(1),(int,float))
        return (str_var in str_func and str_var.isalpha() and test)
    except (TypeError, ValueError):
        return False
    
    

def validate_nR_point0(enter_point):
    try:
        return isinstance(float(enter_point),(int,float))
    except ValueError:
        return False
    

def newtonRaphson_main():
    var=input("var: ")
    func=input("func: ")
    while not validate_function(func,var):
        print("Error: la funcion esta mal escrita o no esta en terminos de la variable ingresada")
        var=input("var again: ")
        func=input("func again: ")

    point=input("point: ")
    while not validate_nR_point0(point):
        point=input("point again: ")

    point=float(point)

    init=time.time()
    result=newtonRapshon(func,var,point,decimal_notation=False)
    end=time.time()

    duration=end-init

    titulo="Newton-Raphson para f({}) = {}".format(var,func)
    tabla=table.getTabla(result,setTitle=titulo)
    print(tabla)
    print(f"Tiempo de ejecicion:{duration:.8f}")

    
newtonRaphson_main()


