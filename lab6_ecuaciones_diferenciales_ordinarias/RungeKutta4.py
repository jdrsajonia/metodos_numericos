import sympy as sp

class RungeKutta:

    def __init__(self,function:str, interval:tuple, h_steps:float,y_0:float ):

        self.expr=sp.sympify(function)
        self.diff_str_function=function
        self.diff_eval_function=sp.lambdify(sp.symbols('t y'), self.expr)

        self.y_0=y_0

        self.h=h_steps
        self.a,self.b=interval

        self.M_subintervals=int((self.b-self.a)/self.h)


    def set_h(self,h):
        self.h=h

    def solve_by_rk4(self):
        
        function=self.diff_eval_function
        h=self.h
        y_k=self.y_0
        t_k_list=[self.a + k*self.h for k in range(self.M_subintervals+1)]

        results={"t_k":t_k_list, "y_k":[]}

        for t_k in t_k_list:
        
            f_1=function(t_k, y_k)
            f_2=function(t_k+h/2, y_k+(h/2)*f_1)
            f_3=function(t_k+h/2, y_k+(h/2)*f_2)
            f_4=function(t_k+h, y_k+h*f_3)

            y_k1=y_k+(f_1+2*f_2+2*f_3+f_4)*h/6

            results["y_k"].append(y_k) 
            y_k=y_k1                   #actualiza el valor de y_k

        return results
    

