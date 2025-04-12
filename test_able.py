import random
import string
import generate_table as table
def generar_diccionario(num_claves, longitud_listas):
    diccionario = {}
    
    for _ in range(num_claves):
        nombre_random = ''.join(random.choices(string.ascii_letters, k=8))  # 8 letras al azar
        lista_flotantes = [round(random.uniform(0, 100), 30) for _ in range(longitud_listas)]
        diccionario[nombre_random] = lista_flotantes
    
    return diccionario

# Generar un diccionario dadas x, y dimensiones
entrada=input("set dimension | x | y |: ").split(" ")
entrada=list(map(int,entrada))
print(entrada)
resultado = generar_diccionario(num_claves=entrada[0], longitud_listas=entrada[1])

print(resultado)
tabla=table.getTabla(resultado)
print(tabla)
