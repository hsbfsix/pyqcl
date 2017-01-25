#Quantum teleportation: make Dest the same state as Source

import numpy as np
from pyqcl import *

Source = QubitSystem().make([0,1], [np.sqrt(1./3.), np.sqrt(2./3.)])
print("Source: ", Source)
Inter = QubitSystem().make([0, 1], [1, 0])
Dest = QubitSystem().make([0, 1], [1, 0])
System = Source.add_qubit(Inter).add_qubit(Dest)

#Turn the lower qubits from |00> to Bell_00

Bell = HadamardGate().kronecker(IGate()).composit(CNOTGate())
SystemBell = IGate().kronecker(Bell)
System = SystemBell(System)

#Apply CNOT to Source and Inter

SystemCNOT = CNOTGate().kronecker(IGate())
System = SystemCNOT(System)

#Apply Hadamard transfrom to Source

SystemHT = HadamardGate().kronecker(IGate()).kronecker(IGate())
System = SystemHT(System)

#Measure Source

M1 = System.measure_single(0)

#Measure Inter on reduced System

M2 = System.measure_single(0)

#System is now just Dest, since the other two have been measured

#if M2 is 1 apply X gate to System

if M2 == 1:
    X = XGate()
    System = X(System)

#if M1 is 1 apply Z gate to System

if M1 == 1:
    Z = ZGate()
    System = Z(System)

#print Dest. This is technically cheating, but eh.

print("\nDest: ", System)