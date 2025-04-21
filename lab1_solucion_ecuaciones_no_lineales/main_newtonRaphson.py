from modules import newton_raphson as nr
from modules import generate_table as t
import time

# flujo del programa:
def main_newtonRaphson():
    var=input("Inserte una variable independiente (x,y,z,w... etc)\n(Ejemplo: Variable = x )\nVariable = ")
    func=input(f"Inserte una funcion continua f({var}) en terminos de {var}\n f({var}) = ")

    while not nr.validate_function(func,var):
        print("\nError: La funcion no es valida, intente otra vez:")
        var=input("Variable = ")
        func=input(f"f({var}) = ")

    point=input("Punto inicial\nP = ")
    while not nr.validate_nR_point0(point):
        print(f"\nError: {point} no es válido, intente otra vez:")
        point=input("P = ")

    point=float(point)

    init=time.time()
    result=nr.newtonRaphson(func,var,point,decimal_notation=False)
    end=time.time()

    duration=end-init

    titulo="Newton-Raphson para f({}) = {}".format(var,func)
    tabla=t.getTabla(result,setTitle=titulo)
    print(tabla)
    print(f"Tiempo de ejecicion:{duration:.8f}")
    nr.graficar_nr(func,var,results=result)

main_newtonRaphson()


