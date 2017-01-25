import numpy as np
from pyqcl import *

#Deutsch-Jozsa algorithm: find whether given function is const or balanced
# for N bits

def balanced(num):
    return num % 2

def constant(num):
    return 1

N = int(input("Enter N: "))

#N |0> qubits and one |1> qubit for target

Qarr = [QubitSystem().make([0,1], [1,0]) for i in range(N - 1)]
Query = QubitSystem().make([0,1], [1,0])
for q in Qarr:
    Query.add_qubit(q)
Ans = QubitSystem().make([0,1], [0,1])
System = Query.add_qubit(Ans)

#Apply Hadamard transform to whole bunch

SystemHT = HadamardGate(N + 1)
System = SystemHT(System)

#Apply func. THIS IS THE INPUT.

System.apply_func_last(constant)

#Apply Hadamard transform to Query

SystemHTQuery = HadamardGate(N).kronecker(IGate())
System = SystemHTQuery(System)

#Measure Query. If all 0 then constant, otherwise balanced

for i in range(N):
    if System.measure_single(0) != 0:
        print("Balanced")
        break
else:
    print("Constant")