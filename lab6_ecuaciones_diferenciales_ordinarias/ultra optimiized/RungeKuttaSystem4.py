import sympy as sp
import getTabla as table

class RungeKuttaSystem:
        
    '''
    Implementa el método de Runge-Kutta de orden 4 para resolver sistemas de EDOs de primer orden
    de la forma:

            dx/dt = f(t, x, y)
            dy/dt = g(t, x, y)

    Requiere funciones f y g como strings, así como condiciones iniciales para x y y.
    '''
        


    def __init__(self,function1:str, function2:str, interval:tuple, h_steps:float,x_0:float, y_0:float ):
        """
        Inicializa el sistema con las funciones diferenciales y condiciones iniciales.

        Args:
            function1 (str): Expresión de dx/dt = f(t, x, y).
            function2 (str): Expresión de dy/dt = g(t, x, y).
            interval (tuple): Intervalo de integración (a, b).
            h_steps (float): Paso de integración h.
            x_0 (float): Valor inicial de x en t = a.
            y_0 (float): Valor inicial de y en t = a.
        """
        self.expr1=function1
        self.expr2=function2

        t,x,y = sp.symbols('t x y')
        self.diff_eval_function1=sp.lambdify((t, x, y), self.expr1)
        self.diff_eval_function2=sp.lambdify((t, x, y), self.expr2)

        self.x_0=x_0
        self.y_0=y_0

        self.h=h_steps
        self.a,self.b=interval

        self.M_subintervals=int((self.b-self.a)/self.h)


    def set_h(self,h):
        """
        Permite actualizar el paso de integración h y recalcula el número de subintervalos.

        Args:
            h (float): Nuevo paso de integración.
        """
        self.h=h
        self.M_subintervals=int((self.b-self.a)/self.h)

    def solve_by_rk4(self):
        """
        Resuelve el sistema de EDOs mediante el método de Runge-Kutta de orden 4 (RK4).

        Returns:
            dict: Un diccionario con las listas:
                - "k": índices de iteración
                - "t_k": valores de t
                - "x_k": aproximaciones de x(t)
                - "y_k": aproximaciones de y(t)
        """
        
        function1=self.diff_eval_function1
        function2=self.diff_eval_function2

        h=self.h

        x_k=self.x_0
        y_k=self.y_0

        t_k_list=[(self.a + k*self.h) for k in range(self.M_subintervals+1)]
        k_iterations=list(range(len(t_k_list)))

        results={"k":k_iterations, "t_k":t_k_list, "x_k":[]}

        for t_k in t_k_list:
            
            # aplicacion iterativa de las formulas para sistemas acoplados
            f_1, g_1 = (function1(t_k, x_k, y_k),                           function2(t_k, x_k, y_k))
            f_2, g_2 = (function1(t_k+h/2, x_k+(h/2)*f_1, y_k+(h/2)*g_1),   function2(t_k+h/2, x_k+(h/2)*f_1, y_k+(h/2)*g_1))
            f_3, g_3 = (function1(t_k+h/2, x_k+(h/2)*f_2, y_k+(h/2)*g_2),   function2(t_k+h/2, x_k+(h/2)*f_2, y_k+(h/2)*g_2))
            f_4, g_4 = (function1(t_k+h, x_k+h*f_3, y_k+h*g_3),             function2(t_k+h, x_k+h*f_3, y_k+h*g_3)) 
            
            x_k1 = x_k + (f_1+2*f_2+2*f_3+f_4)*h/6
            y_k1 = y_k + (g_1+2*g_2+2*g_3+g_4)*h/6

            results["x_k"].append(x_k)

            x_k=x_k1
            y_k=y_k1                   #actualiza el valor de x_k, y_k

        return results
    
