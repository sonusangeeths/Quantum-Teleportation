# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 19:54:48 2024

@author: sonusangeeths
"""

from qiskit import *
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
from qiskit_aer import Aer

qc = QuantumCircuit(3,2)

#generation of bell states
qc.h(1)
qc.cx(1,2)

qc.u(30, 60, 60, 0) #Build a random qubit
state_1 = Statevector(qc)
qc.barrier()

qc.cx(0, 1)
state_2 = Statevector(qc)
qc.barrier()

qc.h(0)
state_3 = Statevector(qc)
qc.barrier()

qc.cx(0,2)
qc.cz(1,2)

qc.measure(0, 0)
qc.measure(1, 1)

#bob applies conditional statement
qc.z(2).c_if(qc.clbits[0],1)
qc.x(2).c_if(qc.clbits[1],1)

qc.draw(output = 'mpl')

#running the simulation
qc.save_statevector()
sim = Aer.get_backend('aer_simulator')
res = sim.run(qc,shots = 1024).result()

#final state after simulation
final_state = res.get_statevector(qc)

#plot the bloch sphere of final state
plot_bloch_multivector(final_state)