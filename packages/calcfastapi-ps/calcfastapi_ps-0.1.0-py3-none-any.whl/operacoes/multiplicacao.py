from operacoes.base import Operacao

class Multiplicacao(Operacao):
    def calcular(self, a: float, b: float) -> float:
        return a * b
