import sympy as sp
import RungeKuttaSystem4 as rk
import getTabla as table

class EDOsuperior:
    '''
    Recibe una ecuacion mx''(t) + cx'(t) + kx(t) - g(t) = 0
    y despeja x''(t).

    La entrada de la ecuación debe seguir un formato.

    ddx = x''(t)
    dx = x'(t)
    x = x(t)

    Por lo tanto, la entrada en string para una ecuación diferencial igualada a sero es:
    input>> m*ddx + c*dx + k*x - g
    Nota: m, c, k, g; pueden ser constantes o funciones de t.

    '''

    def __init__(self, ecuation:str):
        """
        Inicializa la ecuación diferencial de segundo orden.

        Args:
            ecuation (str): Ecuación en notación simbólica con 'ddx', 'dx' y 'x'.
        """
        self.ecuation=ecuation

    def _clear_second_derivate(self):
        """
        Despeja la segunda derivada (ddx) de la ecuación.

        Returns:
            str: Expresión de ddx despejada, como string.
        """
        ecuation=self.ecuation
        ddx = sp.Symbol("ddx")

        expr = sp.sympify(ecuation)
        solution = sp.solve(expr, ddx)[0]
        return str(solution)

    
    def do_substitution(self):
        """
        Sustituye dx por y en la expresión despejada de ddx, para reducir el orden de la EDO.

        Returns:
            str: Ecuación reducida con dx → y.
        """
        
        solution_expr = sp.sympify(self._clear_second_derivate())
        solution_substituted = solution_expr.subs(sp.Symbol("dx"), sp.Symbol("y"))
        return str(solution_substituted)


    def solve(self,interval:tuple, h_steps:float, x_0:float, y_0:float):

        ecuation_replaced=self.do_substitution()
        system=rk.RungeKuttaSystem("y", ecuation_replaced, interval, h_steps, x_0, y_0)
        results=system.solve_by_rk4()
        return results

    





# edo=EDOsuperior("ddx + 4*dx + 5*x")

# # edo=EDOsuperior("ddx - t*dx + t*x - t")
# print(edo.do_substitution())

# results=edo.solve((0,5), 0.1, 3, -5)

# print(table.getTabla(results))

# # # results=edo.sistema("x+2*y", "3*x+2*y" ,(0,0.2), 0.02, 6, 4)

