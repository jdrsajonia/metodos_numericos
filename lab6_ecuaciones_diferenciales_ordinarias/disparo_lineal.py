import EDOsuperior as edos
import getTabla as table
class ShootLineal:
    """
    Resuelve problemas de contorno para EDOs de segundo orden usando el método de disparo lineal.
    Utiliza la clase EDOsuperior para resolver el sistema asociado.
    """

    def __init__(self, ecuacion:str, intervalo:tuple, h:float, alpha:float, beta:float):
        """
        Args:
            ecuacion (str): Ecuación diferencial en el formato de EDOsuperior.
            intervalo (tuple): Intervalo (a, b).
            h (float): Paso de integración.
            alpha (float): Condición inicial y(a).
            beta (float): Condición final y(b).
        """
        self.ecuacion = ecuacion
        self.intervalo = intervalo
        self.h = h
        self.alpha = alpha
        self.beta = beta

    

    def solve(self):
        """
        Resuelve el problema de contorno usando el método de disparo lineal.
        """
        a, b = self.intervalo

        # Primer disparo: y(a)=alpha, y'(a)=0
        edo1 = edos.EDOsuperior(self.ecuacion)
        res1 = edo1.solve(self.intervalo, self.h, self.alpha, 0)
        y1b = res1["x_k"][-1]

        # Segundo disparo: y(a)=alpha, y'(a)=1
        edo2 = edos.EDOsuperior(self.ecuacion)
        res2 = edo2.solve(self.intervalo, self.h, self.alpha, 1)
        y2b = res2["x_k"][-1]

        # Factor de combinación
        s = (self.beta - y1b) / (y2b - y1b)

        # Construir solución final por combinación lineal
        t_k = res1["t_k"]
        y_sol = []
        dy_sol = []
        for i in range(len(t_k)):
            y  = res1["x_k"][i] + s * (res2["x_k"][i] - res1["x_k"][i])
            dy = res1["y_k"][i] + s * (res2["y_k"][i] - res1["y_k"][i])
            y_sol.append(y)
            dy_sol.append(dy)

        # ← aquí, ya fuera del for, devuelves TODO el diccionario
        return {
            "t_k":   t_k,
            "y_k":   y_sol,
            "y'_k":  dy_sol
        }

    


shoot = ShootLineal("ddx - (2*t)/(1+t**2)*dx + 2/(1+t**2) - 1", (0,4), 0.1, 1.25, -0.95)

results=shoot.solve()
print(results)
print(table.getTabla(results))