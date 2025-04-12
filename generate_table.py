def getTabla(heads_data,character="-"):
    '''
        Esta funcion genera una tabla para almacenar y mostrar los datos recolectados
        en los laboratorios que necesiten implementar este formato para la materia de Métodos Numéricos.

        A continuación se describe la documentación de la función, la cual se espera, sea reutilizada a lo largo del curso.

        tabla(head_data, character="-"): es una función que recibe un diccionario y retorna un string; la tabla de valores con dimensiones n x m
        (de forma opcional recibe un parámetro character, para formatear los espacios entre los valores y las columnas)

            table: es una variable acumuladora de strings, guardando las lineas generadas
            long_elements_x: es un diccionario que guarda la longitud mas grande para cada columna de la tabla
            first_head: guarda la primera llave del diccionario head_data para obtener la altura -y- de las columnas de la tabla
            long_tabla_y: obtiene el tamaño total en -y- de la tabla
            long_tabla_x: obtiene el tamaño total en -x- de la tabla
            enmarcate: obtiene la enmarcacion de la tabla con caracteres = con su longitud proporcional 
        
        Nota: al usar esta funcion, hay que asegurarse que las listas de cada llave, tengan la misma longitud para garantizar
        la integridad del codigo y de la informacion. De lo contario, el codigo arrojará un Index Out Of Bounds

    '''
    table=""
    long_elements_x=dict()

    if len(character)>1:
        character=character[:1]

    for head in heads_data: 
        # Este for consigue los mayores anchos necesarios para cada columna de la tabla, para mantener un formato
        long_element_x=max(map(str,heads_data[head]),key=len)
        long_head=len(head)
        long_data=len(long_element_x)
        long_elements_x[head]=max(long_head,long_data) 

    first_head=next(iter(heads_data))

    long_tabla_y=len(heads_data[first_head])
    long_tabla_x=sum(long_elements_x.values())
    enmarcate=long_tabla_x+2*len(heads_data)+len(heads_data)+1
    
    table +="\n"+"="*enmarcate+"\n"+"|"

    for head in heads_data:
        # Este for carga los encabezados de la tabla
        tabulate=long_elements_x[head]
        text_head=str(head).center(tabulate,character)
        table+=" "+text_head+" |"

    table+="\n"+"="*enmarcate+"\n"

    for i in range(long_tabla_y):
        # Este for carga los datos obtenidos a la tabla
        table+="|"
        for head in heads_data:
            tabulate=long_elements_x[head]
            text_data=str(heads_data[head][i]).center(tabulate,character)
            table+=" "+text_data+" |"
        table+="\n"

    table+="="*enmarcate
    return table
    

#data={"k":[1,2,3,4,5],"texto 1":[0.123,0.99,0.1,5,4.99923], "texto 2C":[2,0.78,231,3322,3], "txt39999999":[4,2,1,0.1,88],"txt":[2,3,4,1,5]}
#example=getTabla(data)
#print(example)


