'''from newton_raphson import newtonRaphson 
import generate_table as t

newtonRapshonFunctions = [
    ("x**2 - 2", 1.0),
    ("x**3 - x - 2", 1.5),
    ("cos(x) - x", 1.0),
    ("x * exp(x) - 1", 0.5),
    ("x**3 - 2*x + 2", -2.0),
    ("x*sin(x) - 1", 2)
]

for func, point in newtonRapshonFunctions:
    result=newtonRaphson(func,"x",point,decimal_notation=True)
    print(t.getTabla(result,setTitle="f(x) = {} at P = {}".format(func,point)))'''
