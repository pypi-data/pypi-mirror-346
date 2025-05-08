from operacoes.base import Operacao

class Soma(Operacao):
    def calcular(self, a: float, b: float) -> float:
        return a + b
