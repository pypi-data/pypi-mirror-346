from operacoes.base import Operacao

class Divisao(Operacao):
    def calcular(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Não é possível dividir por zero.")
        return a / b
