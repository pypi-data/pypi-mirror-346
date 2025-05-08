from operacoes.base import Operacao

class Subtracao(Operacao):
    def calcular(self, a: float, b: float) -> float:
        return a - b
