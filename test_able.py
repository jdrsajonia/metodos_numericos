import random
import string
import generate_table as table
def generar_diccionario(num_claves, longitud_listas):
    diccionario = {}
    
    for _ in range(num_claves):
        # Generar un nombre aleatorio para la clave
        nombre_random = ''.join(random.choices(string.ascii_letters, k=8))  # 8 letras al azar
        # Generar una lista de números flotantes con la longitud dada
        lista_flotantes = [round(random.uniform(0, 100), 30) for _ in range(longitud_listas)]
        # Agregar al diccionario
        diccionario[nombre_random] = lista_flotantes
    
    return diccionario

# Generar un diccionario con 5 claves, y listas de tamaño 10
resultado = generar_diccionario(num_claves=8, longitud_listas=9)

print(resultado)
table.tabla(resultado)
#NOTA: este script fue creado con ChatGPT