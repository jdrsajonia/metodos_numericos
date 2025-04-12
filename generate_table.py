def tabla(heads_data):

    long_elements_x=dict()

    for head in heads_data: # Este for consigue los mayores anchos necesarios para cada columna de la tabla, para mantener un formato
        long_element_x=max(map(str,heads_data[head]),key=len)
        long_head=len(head)
        long_data=len(long_element_x)
        long_elements_x[head]=max(long_head,long_data) 

    first_head=next(iter(heads_data))

    long_tabla_y=len(heads_data[first_head])
    long_tabla_x=sum(long_elements_x.values())
    enmarcate=long_tabla_x+2*len(heads_data)+len(heads_data)+1

    print("\n"+"="*enmarcate)

    print("|",end="") 

    for head in heads_data:
        tabulate=long_elements_x[head]
        text_head=str(head).center(tabulate,"-")
        print(" "+text_head,end=" |")

    print("\n"+"="*enmarcate)
   

    for i in range(long_tabla_y):
        print("|",end="")
        for head in heads_data:
            tabulate=long_elements_x[head]
            text_data=str(heads_data[head][i]).center(tabulate,"-")
            print(" "+text_data,end=" |")
        print()

    print("="*enmarcate)
    

data={"k":[1,2,3,4,5],"texto 1":[0.123,0.99,0.1,5,4.99923], "texto 2C":[2,0.78,231,3322,3], "txt39999999":[4,2,1,0.1,88],"txt":[2,3,4,1,5]}



