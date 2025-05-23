class Iteration:
    count = 0
    iterations = []
    # Constructor:
    def __init__(self, P):
        Iteration.iterations.append(self)
        self.id = Iteration.count
        self.P = P
        Iteration.count += 1

    # Método de impresión.
    def __str__(self):
        valores = '\t'.join(f"{x:.6f}" for x in self.P)  # 6 decimales, puedes ajustar
        return f"Iteración: {self.id}\t{valores}"
    
    @staticmethod
    def last(x):
        return Iteration.iterations[-1].P[x]