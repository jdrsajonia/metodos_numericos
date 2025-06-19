import numpy as np

class SistemaLinealLU:
    def __init__(self,A:np.ndarray,B:np.ndarray):
        if not isinstance(A,np.ndarray) or not isinstance(B,np.ndarray):
            raise TypeError("A y B deben ser objetos np.ndarray")
        if A.shape[0]!=A.shape[1]:
            raise ValueError("La matriz A debe ser cuadrada")
        if A.shape[0]!=B.shape[0]:
            raise ValueError("Dimensión de B incompatible con A")
        if np.isclose(np.linalg.det(A),0):
            raise ValueError("La matriz A no tiene solución única")
        self.A=A.astype(float)
        self.B=B.astype(float)
        self.L=None
        self.U=None

    def _es_triangular_superior(self,M):
        return np.allclose(M,np.triu(M))

    def _es_triangular_inferior(self,M):
        return np.allclose(M,np.tril(M))

    def _sustitucion_regresiva(self,U,y):
        n=U.shape[0]
        x=[0.0]*n
        x[-1]=y[-1]/U[-1,-1]
        for i in range(n-2,-1,-1):
            x[i]=(y[i]-np.dot(U[i,i+1:],x[i+1:]))/U[i,i]
        return x

    def _sustitucion_progresiva(self,L,b):
        n=L.shape[0]
        y=[0.0]*n
        y[0]=b[0]/L[0,0]
        for i in range(1,n):
            y[i]=(b[i]-np.dot(L[i,:i],y[:i]))/L[i,i]
        return y

    def factorizar(self):
        A=self.A.copy()
        n=A.shape[0]
        L=np.eye(n)
        U=A.copy()
        for j in range(n):
            if np.isclose(U[j,j],0):
                raise ValueError(f"Pivote cero en fila {j}, se requiere pivoteo.")
            for i in range(j+1,n):
                m_ij=U[i,j]/U[j,j]
                U[i]=U[i]-m_ij*U[j]
                L[i,j]=m_ij
        self.L=L
        self.U=U

    def resolver(self):
        if self.L is None or self.U is None:
            self.factorizar()
        y=self._sustitucion_progresiva(self.L,self.B)
        x=self._sustitucion_regresiva(self.U,y)
        return np.array(x)


a=np.array([[92,20],[20,8]])
b=np.array([[25],[37]])

linalsystem=SistemaLinealLU(a,b)
sol=linalsystem.resolver()
print(sol)