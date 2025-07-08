import sympy as sp
import RungeKuttaSystem4 as rk

class ShootLineal:
    """
    Implementa el método de disparo lineal para resolver problemas de contorno
    en ecuaciones diferenciales ordinarias de segundo orden.

    La EDO debe ingresarse en forma simbólica como string:
        m*ddx + c*dx + k*x - g(t) = 0
    donde:
        - ddx representa x''(t)
        - dx representa x'(t)
        - x  representa x(t)

    Se basa en transformar la EDO de segundo orden en un sistema de primer orden
    y aplicar Runge-Kutta para obtener la solución.
    """

    def __init__(self, ecuation:str, interval:tuple, h_step:float, alpha:float, betha:float):
        """
        Inicializa los parámetros del problema de contorno.

        Args:
            ecuation (str): Ecuación diferencial en formato simbólico.
            interval (tuple): Intervalo de integración (a, b).
            h_step (float): Paso de integración h.
            alpha (float): Condición inicial x(a) = α.
            betha (float): Condición final x(b) = β.
        """
        self.ecuation=ecuation
        self.interval=interval
        self.h=h_step

        self.alpha=alpha
        self.betha=betha 

        self.ddx_ecuation=self.clear_second_derivate(self.ecuation)
        self.ddx_ecuation_without_g=self.clear_second_derivate_without_g(self.ecuation)

        pass

    def clear_second_derivate(self, ecuation:str):
        """
        Despeja la segunda derivada ddx de la ecuación completa (incluyendo g(t)).

        Args:
            ecuation (str): EDO en forma simbólica.

        Returns:
            Expr: Ecuación despejada para ddx.
        """

        ddx= sp.symbols("ddx")
        expresion=sp.sympify(ecuation)

        # print(expresion.args)
        solution=sp.solve(expresion,ddx)[0]
        return solution


    def clear_second_derivate_without_g(self, ecuation):
        """
        Despeja ddx de la ecuación sin el término g(t),
        útil para construir la solución base v(t) con condición inicial x'(a)=1, x(a)=0.

        Args:
            ecuation (str): EDO simbólica.

        Returns:
            Expr: Ecuación para ddx sin el término g(t).
        """

        ddx, dx, x= sp.symbols("ddx dx x")
        expresion=sp.sympify(ecuation)

        new_expresion_without_g=sum([term for term in expresion.args if term.has(ddx) or term.has(dx) or term.has(x)])

        solution=sp.solve(new_expresion_without_g, ddx)[0]
        return solution
    
    def do_substitution(self):
        """
        Sustituye dx por y en ambas ecuaciones despejadas, con y = x'(t),
        para transformar el sistema en dos EDOs de primer orden.
        """
        
        self.ddx_ecuation=self.ddx_ecuation.subs(sp.Symbol("dx"), sp.Symbol("y"))
        self.ddx_ecuation_without_g=self.ddx_ecuation_without_g.subs(sp.Symbol("dx"), sp.Symbol("y"))


    def solve_U_EDOsuperior(self):
        """
        Resuelve el sistema asociado a la solución particular u(t),
        usando las condiciones iniciales x(a)=α, x'(a)=0.

        Returns:
            dict: Diccionario con resultados para t_k, x_k y y_k.
        """

        self.do_substitution()
        system=rk.RungeKuttaSystem("y", self.ddx_ecuation, self.interval, self.h, self.alpha, 0)
        results=system.solve_by_rk4()

        return results
    
    def solve_V_EDOsuperior(self):
        """
        Resuelve el sistema asociado a la solución homogénea v(t),
        usando condiciones iniciales x(a)=0, x'(a)=1.

        Returns:
            dict: Diccionario con resultados para t_k, x_k y y_k.
        """

        self.do_substitution()
        system=rk.RungeKuttaSystem("y", self.ddx_ecuation_without_g, self.interval, self.h, 0, 1)
        results=system.solve_by_rk4()

        return results
    
    def solve_by_shoot(self):
        """
        Ejecuta el método de disparo lineal combinando u(t) y v(t)
        para satisfacer la condición final x(b) = β.

        Returns:
            dict: Diccionario con las claves:
                - "t_k": valores del tiempo
                - "x_k": solución aproximada x(t) en cada paso
        """

        results={"t_k":[], "x_k":[]}

        u_result = self.solve_U_EDOsuperior()
        v_result = self.solve_V_EDOsuperior()

        u_sucesion=u_result["x_k"]
        v_sucesion=v_result["x_k"]

        results["t_k"]=u_result["t_k"]        

        c=(self.betha-u_sucesion[-1])/v_sucesion[-1]

        for u, v in zip(u_sucesion, v_sucesion):   
            x_k=u+c*v
            results["x_k"].append(x_k)
        return results
    








