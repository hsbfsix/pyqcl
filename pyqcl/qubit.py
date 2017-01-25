import numpy as np

EPSILON = 0.000005


class LawOfNatureException(Exception):
    def __init__(self):
        print("Sorry, you tried going against the laws of nature.")


class QubitSystem():
    amplitudes = None
    bases = None
    num_qubits = 1

    def __init__(self, number=1, orig=None):
        if (orig != None):
            raise LawOfNatureException

    def make(self, bases, amps):
        self.amplitudes = np.array(amps)

        if np.sum(self.amplitudes ** 2) - 1.0 >= EPSILON:
            raise LawOfNatureException

        self.bases = bases
        return self

    def add_qubit(self, qubit):
        temp_list = []
        for item in self.amplitudes:
            for amp in qubit.amplitudes:
                temp_list += [item * amp]
        self.amplitudes = np.array(temp_list)
        self.bases = self.bases * 2
        for i in range(len(self.bases)):
            self.bases[i] = i
        self.num_qubits += 1
        qubit.measure()
        return self

    def inv_2_order(self):
        self.amplitudes[1], self.amplitudes[3] = self.amplitudes[3], self.amplitudes[1]
        return self

    def partition(self, num):
        run_length = 2 ** (num)
        lt = [i for i in range(len(self.amplitudes))]
        i = 0
        zeros = []
        ones = []
        while i < len(lt):
            c = 0
            while c < run_length:
                zeros += [lt[i]]
                c += 1
                i += 1
            c = 0
            while c < run_length:
                ones += [lt[i]]
                c += 1
                i += 1
        return zeros, ones

    def measure_single(self, qubit_num):
        zeros, ones = self.partition(self.num_qubits - qubit_num - 1)
        self.num_qubits -= 1
        zeros_total_prob = 0
        zeros_amplitudes = []
        for i in zeros:
            zeros_total_prob += self.amplitudes[i] ** 2
            zeros_amplitudes += [self.amplitudes[i]]

        ones_total_prob = 0
        ones_amplitudes = []
        for i in ones:
            ones_total_prob += self.amplitudes[i] ** 2
            ones_amplitudes += [self.amplitudes[i]]

        rand_num = np.random.random()
        if rand_num < zeros_total_prob:
            self.amplitudes = np.array(zeros_amplitudes) / (np.sqrt(zeros_total_prob))
            self.bases = self.bases[:len(self.bases) // 2]
            return 0
        else:
            self.amplitudes = np.array(ones_amplitudes) / (np.sqrt(ones_total_prob))
            self.bases = self.bases[:len(self.bases) // 2]
            return 1

    def measure(self):
        self.num_qubits = 1
        rand_num = np.random.random()
        cdf = []
        s = 0
        for amplitude in self.amplitudes:
            s += amplitude ** 2
            cdf += [s]

        for i, cd in enumerate(cdf):
            if rand_num <= cd:
                for j in range(len(self.amplitudes)):
                    if j == i:
                        self.amplitudes[j] = 1
                    else:
                        self.amplitudes[j] = 0
                return self.bases[i]

    def apply_func_last(self, func):
        reorder_list = []
        for base in self.bases:
            rem = base % 2
            base = base // 2
            c = (base * 2) + (rem + func(base)) % 2
            reorder_list += [c]

        copied = np.copy(self.amplitudes)
        for i in range(len(self.amplitudes)):
            self.amplitudes[i] = copied[reorder_list[i]]

        return self

    def __str__(self):
        string = ""
        for i, amplitude in enumerate(self.amplitudes):
            string += "\nAmp " + str(i) + ": " + str(amplitude)

        for i, basis in enumerate(self.bases):
            string += "\nBasis " + str(i) + ": " + str(basis)

        return string
