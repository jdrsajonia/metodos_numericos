import generate_table as table
import math


def bolzano(function,a,b):

     

    f = lambda x:eval(function)

    for k in range(0,9):
        
        c=(a+b)/2 #punto medio
        f_a = f(a)
        f_b = f(b)
        f_c = f(c) 

        f_a_c = (f_a>0 and f_c<0) or (f_a<0 and f_c>0) # f(a) y f(c) tienen signos opuestos. Si es cierto, (a,c) --> (a,b)
    
        f_c_b = (f_b>0 and f_c<0) or (f_b<0 and f_c>0) # f(b) y f(c) tienen signos opuestos. Si es cierto, (a,c) --> (a,b)

        print(str(k),str(a),str(c),str(b),str(f_c))

        if f_a_c:
            b=c

        elif f_c_b:
            a=c

        elif f(0)==0:
            break  
    
    pass


h="x*math.sin(x)-1"

bolzano(h,0,2)

#data={"k":[1,2,3,4,5],"texto 1":[0.123,0.99,0.1,5,4.99923], "texto 2C":[2,0.78,231,3322,3], "txt39999999":[4,2,1,0.1,88],"txt":[2,3,4,1,5]}
#example=table.getTabla(data)
#print(example)
