import sympy as sp
import getTabla as table
import RungeKuttaSystem4 as rk

class ShootLineal:

    def __init__(self, ecuation:str, interval:tuple, h_step:float, alpha:float, betha:float):

        self.ecuation=ecuation
        self.interval=interval
        self.h=h_step

        self.alpha=alpha
        self.betha=betha 

        self.ddx_ecuation=self.clear_second_derivate(self.ecuation)
        self.ddx_ecuation_without_g=self.clear_second_derivate_without_g(self.ecuation)

        self.u_results=self.solve_U_EDOsuperior()
        self.v_results=self.solve_V_EDOsuperior()

        pass

    def clear_second_derivate(self, ecuation:str):

        ddx= sp.symbols("ddx")
        expresion=sp.sympify(ecuation)

        # print(expresion.args)
        solution=sp.solve(expresion,ddx)[0]
        return solution


    def clear_second_derivate_without_g(self, ecuation):

        ddx, dx, x= sp.symbols("ddx dx x")
        expresion=sp.sympify(ecuation)

        new_expresion_without_g=sum([term for term in expresion.args if term.has(ddx) or term.has(dx) or term.has(x)])

        solution=sp.solve(new_expresion_without_g, ddx)[0]
        return solution
    
    def do_substitution(self):
        """
        Sustituye dx por y en la expresión despejada de ddx, para reducir el orden de la EDO.

        Returns:
            str: Ecuación reducida con dx → y.
        """
        
        self.ddx_ecuation=self.ddx_ecuation.subs(sp.Symbol("dx"), sp.Symbol("y"))
        self.ddx_ecuation_without_g=self.ddx_ecuation_without_g.subs(sp.Symbol("dx"), sp.Symbol("y"))


    def solve_U_EDOsuperior(self):

        self.do_substitution()
        system=rk.RungeKuttaSystem("y", self.ddx_ecuation, self.interval, self.h, self.alpha, 0)
        results=system.solve_by_rk4()

        return results
    
    def solve_V_EDOsuperior(self):

        self.do_substitution()
        system=rk.RungeKuttaSystem("y", self.ddx_ecuation_without_g, self.interval, self.h, 0, 1)
        results=system.solve_by_rk4()

        return results
    
    def solve_by_shoot(self):

        results={"t_k":[], "x_k":[]}

        # u_result = self.solve_U_EDOsuperior()
        # v_result = self.solve_V_EDOsuperior()

        # u_sucesion=u_result["x_k"]
        # v_sucesion=v_result["x_k"]

        # results["t_k"]=u_result["t_k"]

        results["t_k"]=self.u_results["t_k"]

        u_sucesion=self.u_results["x_k"]
        v_sucesion=self.v_results["x_k"]
        


        c=(self.betha-u_sucesion[-1])/v_sucesion[-1]

        for u, v in zip(u_sucesion, v_sucesion):   
            x_k=u+c*v
            results["x_k"].append(x_k)
        return results
    

# a=ShootLineal("ddx - ((2*t)/(1+t**2))*dx + (2/(1+t**2))*x - 1", (0,4), 0.2, 1.25, -0.95)
# result = a.solve_by_shoot()
# print(table.getTabla(result))







