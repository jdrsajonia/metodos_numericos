import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import time 

class NumericIntegration:
    """
    Clase que permite realizar aproximaciones de integrales definidas utilizando
    los métodos numéricos del Trapecio y de Simpson.
    """
    def __init__(self,function,interval,subintervals):
        """
        Constructor de la clase.

        Parametros:
        -----------
        function : str
            Función como string, por ejemplo "x**2 + 3*x".
        interval : tuple
            Intervalo de integración (a, b).
        subintervalss : int
            Número de subintervalos para aproximar la integral.
        """
        self.symbolic_function=sp.sympify(function)
        self.function=sp.lambdify(sp.symbols("x"), function, modules=["numpy"])
        self.interval=interval
        self.subintervals=subintervals
    

    def solve_by_trapezium(self):
        """
        Aplica la Regla del Trapecio para aproximar la integral definida.

        Returns:
        --------
        float : Aproximación numérica de la integral.
        """
        m_nodes=self.subintervals-1
        a,b=self.interval

        h=(b-a)/m_nodes

        x_nodes=[a+k*h for k in range(1,m_nodes)]
        f_points=[self.function(x) for x in x_nodes]

        t_aproximation=(h/2)*(self.function(a)+self.function(b))
        t_aproximation+=+h*sum(f_points)

        return t_aproximation


    def solve_by_simpson(self):
        """
        Aplica la Regla de Simpson compuesta para aproximar la integral definida.

        Returns:
        --------
        float : Aproximación numérica de la integral.
        """

        m_nodes=self.subintervals
        if m_nodes%2!=0:    # si el subintervalo es impar, se vuelve par
            m_nodes=m_nodes-1
        
        a,b=self.interval

        h=(b-a)/(m_nodes)
    
        x_nodes=[a+k*h for k in range(m_nodes+1)]
        f_points=[self.function(x) for x in x_nodes]

        s_aproximation=(h/3)*(self.function(a)+self.function(b))
        s_aproximation+=(2*h/3)*sum(f_points[k] for k in range(2,m_nodes,2))    #x_2k
        s_aproximation+=(4*h)/3*sum(f_points[k] for k in range(1,m_nodes+1,2))  #x_(2k-1)

        return s_aproximation

    def graphic_integration(self):
        """
        Genera una gráfica separada por subplots de las áreas aproximadas por los métodos
        del Trapecio y de Simpson en el intervalo definido.
        """
        a,b=self.interval
        x=np.linspace(a, b, 500)
        y=self.function(x)

        fig,axs=plt.subplots(1, 2, figsize=(12, 5))

        # Trapecio
        m_nodes=self.subintervals - 1
        x_trap=np.linspace(a, b, m_nodes + 1)
        y_trap=self.function(x_trap)
        axs[0].plot(x, y, color='blue', alpha=0.5)
        for i in range(m_nodes):
            xs=[x_trap[i], x_trap[i], x_trap[i+1], x_trap[i+1]]
            ys=[0, y_trap[i], y_trap[i+1], 0]
            axs[0].fill(xs, ys, color='orange', alpha=0.3)
        axs[0].plot(x_trap, y_trap, 'o-', color='orange', label='Area por Trapecios = {:.4f}'.format(self.solve_by_trapezium()))
        axs[0].set_title(f'Aproximación por Trapecios para f(x) = {self.symbolic_function}')
        axs[0].set_xlabel('x')
        axs[0].set_ylabel('f(x)')
        axs[0].legend()

        # Simpson
        m_nodes_simpson=self.subintervals
        if m_nodes_simpson%2!=0:
            m_nodes_simpson-=1
        x_simp=np.linspace(a, b, m_nodes_simpson + 1)
        y_simp=self.function(x_simp)
        axs[1].plot(x, y, color='blue', alpha=0.5)
        for i in range(0, m_nodes_simpson, 2):
            xs=np.linspace(x_simp[i], x_simp[i+2], 100)
            coeffs=np.polyfit(x_simp[i:i+3], y_simp[i:i+3], 2)
            ys=np.polyval(coeffs, xs)
            axs[1].fill_between(xs, ys, color='green', alpha=0.2)
        axs[1].plot(x_simp, y_simp, 'o-', color='green', label='Area por Simpson = {:.4f}'.format(self.solve_by_simpson()))
        axs[1].set_title(f'Aproximación por Simpson para f(x) = {self.symbolic_function}')
        axs[1].set_xlabel('x')
        axs[1].set_ylabel('f(x)')
        axs[1].legend()

        plt.tight_layout()
        plt.show()






def user_input():
    title="="*62+"\nAproximación de Integrales por la Regla del Trapecio y Simpson\n"+"="*62
    msg1="\nIngrese una función en términos de x:"
    msg2="\nIngrese el intervalo [a, b] a evaluar\nEjemplo: [a, b] = 0 5"
    msg3="\nIngrese la cantidad de subintervalos para la integral\nEjemplo: N = 10"
    print(title)
    print(msg1)

    while True:
        try:
            function=str(input(">> f(x) = "))
            test=sp.lambdify(sp.symbols("x"),function)
            test(10)
            break
        except TypeError:
            print("ERROR: La función no es válida, intente de nuevo")

    print(msg2)
    while True:
        try:
            interval=tuple(map(float, input(">> [a, b] = ").strip().split()))
            if len(interval)!=2:
                raise ValueError
            break
        except ValueError:
            print("ERROR: el intervalo no es válido, intente nuevamente.")
    print(msg3)
    while True:
        try:
            subintervals=int(input(">> N = "))
            if subintervals<2:
                raise ValueError
            break
        except ValueError:
            print("ERROR: La cantidad de subintervalos debe ser un entero mayor a 1, intente nuevamente.")
    return function, interval, subintervals



def integration_main(function=None, interval=None, subintervals=None, user_console=True):
    if user_console==True:
        function, interval, subintervals=user_input()
    
    primitive_f=NumericIntegration(function,interval,subintervals)

    init=time.perf_counter()
    trapezium_result=primitive_f.solve_by_trapezium()
    end=time.perf_counter()

    print("\n\n"+"-"*40)
    print(f"POR TRAPECIO: \n∫ {primitive_f.symbolic_function} dx = {trapezium_result}")
    print(f"\nTiempo de ejecución 1: {end-init:.10f}")

    init=time.perf_counter()
    simpson_result=primitive_f.solve_by_simpson()
    end=time.perf_counter()
    print("-"*40)
    print(f"POR SIMPSON: \n∫ {primitive_f.symbolic_function} dx = {simpson_result}")
    print(f"\nTiempo de ejecución 2: {end-init:.10f}")
    print("-"*40)

    primitive_f.graphic_integration()



integration_main()