import numpy as np
from rich.console import Console
from dataclasses import dataclass, field


# ================================================ Gradiente temporar (borrar despues de las pruebas) ===========================================================



console = Console()

@dataclass
class Gradiente:
    """
    Clase que representa una función objetivo y sus métodos de optimización mediante descenso de gradiente.
    Permite aplicar diferentes variantes del descenso de gradiente y visualizar los resultados en tablas.
    """

    f : callable
    grad_f : callable
    x_0 : np.ndarray
    v_0 : np.ndarray
    alpha : float
    iteraciones : int
    epsilon : float
    eta : float
    x_historico : list = field(default_factory=list, init=False)
    data : list = field(default_factory=list, init=False)

    @staticmethod
    def _desempaquetar(func, x_0):
        try:
            return func(*x_0)
        except TypeError:
            return func(x_0)

        

    def reset(self):
        """
        Reinicia el historial de posiciones y datos.
        """
        self.x_historico = []
        self.data = []
    

    #@imprimir_tabla
    def simple(self):
        """
        Realiza el descenso de gradiente estándar para minimizar la función objetivo.
        En cada iteración, actualiza la posición usando el gradiente y almacena el historial de posiciones y normas.
        Imprime una tabla con los resultados de cada iteración.
        
        Retorna:
        - x_historico: Lista con el historial de posiciones x en cada iteración.
        """
        self.reset()
        f = self.f
        grad_f = self.grad_f
        x0 = self.x_0
        lr = self.alpha
        max_iters = self.iteraciones
        epsilon = self.epsilon
        self.x_historico = [x0]
        chico = []
        
        for i in range(max_iters):
            f_i = self._desempaquetar(f, x0)
            grad_f_i = self._desempaquetar(grad_f, x0)
            norm_grad = np.linalg.norm(grad_f_i)
            if norm_grad < epsilon: 
                break
            xi = x0 - lr * grad_f_i
            x0 = xi.copy()
            print(f"Iteración {i+1}: x0 = {x0}, grad_f = {grad_f_i}, norma_grad = {norm_grad}")
            self.x_historico.append(x0)
            self.data.append((i+1, x0.tolist(), norm_grad))
            chico.append(norm_grad)
        self.mas_chico = min(chico)
        self.iteracion_mas_chico = chico.index(self.mas_chico) + 1
        return self.x_historico


    #@imprimir_tabla
    def momentum(self):
        """
        Aplica el método de descenso de gradiente con momentum para minimizar la función objetivo.
        Utiliza un término de velocidad para acelerar la convergencia y almacena el historial de posiciones, normas y velocidades.
        Imprime una tabla con los resultados de cada iteración.
        
        Retorna:
        - x_historico: Lista con el historial de posiciones x en cada iteración.
        """
        self.reset()
        f = self.f
        grad_f = self.grad_f
        x0 = self.x_0
        v0 = self.v_0
        lr = self.alpha
        eta = self.eta
        max_iters = self.iteraciones
        epsilon = self.epsilon
        self.x_historico = [x0]
        chico = []
        for i in range(max_iters):
            f_i = self._desempaquetar(f, x0)
            grad_f_i = self._desempaquetar(grad_f, x0)
            norma_grad = np.linalg.norm(grad_f_i)
            if norma_grad < epsilon:
                break
            vi = eta * v0 + lr * grad_f_i
            xi = x0 - vi
            x0 = xi.copy()
            v0 = vi.copy()
            self.x_historico.append(x0)
            chico.append(norma_grad)
            self.data.append((i+1, x0.tolist(), norma_grad, vi.tolist()))
            print(f"Iteración {i+1}: x0 = {x0}, grad_f = {grad_f_i}, norma_grad = {norma_grad}, velocidad = {vi}")
        self.mas_chico = min(chico)
        self.iteracion_mas_chico = chico.index(self.mas_chico) + 1
        return self.x_historico
    
    
    #@imprimir_tabla
    def nesterov(self):
        """
        Aplica el método de descenso de gradiente con Nesterov para minimizar la función objetivo.
        Utiliza un término de velocidad y calcula el gradiente en la posición adelantada (lookahead).
        Imprime una tabla con los resultados de cada iteración.
        
        Retorna:
        - x_historico: Lista con el historial de posiciones x en cada iteración.
        """
        self.reset()
        f = self.f
        grad_f = self.grad_f
        x0 = self.x_0
        v0 = self.v_0
        lr = self.alpha
        eta = self.eta
        max_iters = self.iteraciones
        epsilon = self.epsilon
        self.x_historico = [x0]
        chico = []
        
        for i in range(max_iters):
            lookahead = x0 - eta * v0
            grad_f_i = self._desempaquetar(grad_f, lookahead)
            norm_grad = np.linalg.norm(grad_f_i)
            if norm_grad < epsilon:
                break
            vi = eta * v0 + lr * grad_f_i
            xi = x0 - vi
            x0 = xi.copy()
            v0 = vi.copy()
            self.x_historico.append(x0)
            self.data.append((i+1, x0.tolist(), norm_grad, vi.tolist()))
            chico.append(norm_grad)
            print(f"Iteración {i+1}: x0 = {x0}, grad_f = {grad_f_i}, norma_grad = {norm_grad}")
        self.mas_chico = min(chico)
        self.iteracion_mas_chico = chico.index(self.mas_chico) + 1
        print(f"Iteración con menor norma del gradiente: en la iteración: {self.iteracion_mas_chico} con valor {self.mas_chico}")
        
        return self.x_historico