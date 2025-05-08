from abc import ABC, abstractmethod

class Operacao(ABC):
    @abstractmethod
    def calcular(self, a: float, b: float) -> float:
        pass
