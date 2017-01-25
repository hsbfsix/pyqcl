import numpy as np
from .qubit import QubitSystem, LawOfNatureException

class QuantumGate:
    matrix = None
    num_gates = 1

    def gen_matrix(self, number):
        pass

    def __init__(self, number=1):
        self.matrix = self.gen_matrix(number)

    def apply_to(self, qubit):
        qubit.amplitudes = qubit.amplitudes.dot(self.matrix)
        return qubit

    def composit(self, qgate):
        self.matrix = self.matrix.dot(qgate.matrix)
        return self

    def kronecker(self, qgate):
        self.num_gates += 1
        self.matrix = np.kron(self.matrix, qgate.matrix)
        return self

    def __mul__(self, qubit):
        if isinstance(qubit, QubitSystem):
            return self.apply_to(qubit)
        else:
            raise LawOfNatureException

    def __call__(self, qubit):
        return self.__mul__(qubit)


class XGate(QuantumGate):
    def gen_matrix(self, number):
        return np.array([[0, 1], [1, 0]])


class IGate(QuantumGate):
    def gen_matrix(self, number):
        return np.eye(2)


class ZGate(QuantumGate):
    def gen_matrix(self, number):
        return np.array([[1, 0], [0, -1]])


class HadamardGate(QuantumGate):
    def gen_matrix(self, number):
        h = np.array([[1, 1], [1, -1]]) * np.sqrt(0.5)
        for i in range(number - 1):
            h = np.kron(h, np.array([[1, 1], [1, -1]]) * np.sqrt(0.5))
        return h


class CNOTGate(QuantumGate):
    def gen_matrix(self, number):
        return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])


class ICNOTGate(QuantumGate):
    def gen_matrix(self, number):
        return np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]])
