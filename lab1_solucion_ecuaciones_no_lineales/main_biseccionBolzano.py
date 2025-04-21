from modules import biseccion_bolzano as bb
from modules import generate_table as t
import time


# flujo del programa:
def bolzano_main():
    var=input("Inserte una variable independiente (x,y,z,w... etc)\n(Ejemplo: Variable = x )\nVariable = ")
    func=input(f"Inserte una funcion f({var}) en terminos de {var}\n f({var}) = ")

    while not bb.validate_function(func,var):
        print("\nError: La funcion no es valida, intente otra vez:")
        var=input("Variable = ")
        func=input(f"f({var}) = ")

    interval=input("Inserte el intervalo a b en una sola linea\n(Ejemplo: Intervalo = 3 9 )\nIntervalo = ")
    while not bb.validate_bolzano_interval(func,var,interval):
        interval=input("Intervalo = ")

    interval=interval.split()
    a=float(interval[0])
    b=float(interval[1])


    init=time.time()
    result=bb.bolzano(func,var,a,b)
    end=time.time()

    duracion=end-init

    titulo="Biseccion de Bolzano para f({}) = {}".format(var,func)
    tabla=t.getTabla(result,setTitle=titulo)
    print(tabla)
    print(f"Tiempo de ejecucion: {duracion:.8f}")
    bb.graficar_bb(func,var,results=result)

bolzano_main()