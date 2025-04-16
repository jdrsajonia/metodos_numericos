import sympy as sp #instalar con pip install
from math import *
import generate_table as table

def newtonRapshon(str_function, variable, point_k0):

    results={"k":[],"P_k":[],"(P_k+1)-(P_k)":[],"f(P_k)":[]}

    def derivada(function, variable):
        x=sp.Symbol(variable)
        f=eval(function)  
        derivate_f=sp.diff(f,x)
        return str(derivate_f)
    
    f = lambda x: eval(str_function) # f(x)
    f_diff =lambda x: eval(derivada(str_function,variable)) # f´(x)


    for k in range(0,9):

        f_pk=f(point_k0) # f(pk)
        f_diff_pk=f_diff(point_k0) # f´(pk)
        
        point_k1=point_k0-(f_pk/f_diff_pk)
        #print(k,point_k0,point_k1-point_k0, f_pk)
        difference=abs(point_k1-point_k0)

        results["k"].append(k)
        results["P_k"].append(point_k0)
        results["(P_k+1)-(P_k)"].append(difference)
        results["f(P_k)"].append(f_pk)
        
        #print(f"{k} {point_k0:.6f} {point_k1 - point_k0:.6f} {f_pk:.6f} {f_diff_pk:.6f}")

        point_k0=point_k1

    return results
    
    


#resultados=newtonRapshon("1980*(1-m.e**(-x/10))-98*x","x",16)
#resultados = newtonRapshon("sp.log(x) - 1", "x", 7)

#print(table.getTabla(resultados))
'''
def derivada(function, variable):
        x=sp.Symbol(variable)
        f=eval(function,{"sp":sp, variable:x})  
        derivate_f=sp.diff(f,x)
        return derivate_f
'''


def derivada1(expr_str, var_str):
    x = sp.Symbol(var_str)
    f = sp.sympify(expr_str)
    return str(sp.diff(f, x))

#print(derivada("log(x)", "x"))



#print(derivada1("1980*(1-e**(-x/10))-98*x","x"))

print(str(derivada1("log(x)","x")))
print(str(derivada1("1980*(1-e**(-x/10))-98*x","x")))

f = lambda x: eval(str(derivada1("log(x)","x")))
print(f(1),f(2),f(10))
g = lambda x: eval(str(derivada1("1980*(1-e**(-x/10))-98*x","x")))
print(g(16),g(16.2),g(16.10))

#def g(x):
#     return 1980*(1-m.e**(-x/10))-98*x

#print(g(16))