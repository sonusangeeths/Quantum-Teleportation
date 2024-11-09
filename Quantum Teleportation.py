# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 19:54:48 2024

@author: sonusangeeths
"""

# Importing necessary libraries from Qiskit
from qiskit import *                           # Import core Qiskit functionalities
from qiskit.quantum_info import Statevector     # To create and manipulate state vectors
from qiskit.visualization import plot_bloch_multivector # For visualizing quantum states on the Bloch sphere
from qiskit_aer import Aer                      # Aer package for running quantum simulations

# Initialize a quantum circuit with 3 qubits and 2 classical bits
qc = QuantumCircuit(3, 2)

# Generation of Bell states
qc.h(1)        # Apply Hadamard gate on qubit 1 to create superposition
qc.cx(1, 2)    # Apply CNOT gate with qubit 1 as control and qubit 2 as target to entangle them

# Apply a random unitary gate to create a custom state on qubit 0
qc.u(30, 60, 60, 0)  # The U gate is parameterized with arbitrary angles (theta=30, phi=60, lambda=60)
state_1 = Statevector(qc)  # Save the state vector after creating the custom qubit
qc.barrier()               # Add a barrier to visually separate sections

# Entangle qubit 0 with qubit 1
qc.cx(0, 1)    # Apply CNOT with qubit 0 as control and qubit 1 as target
state_2 = Statevector(qc)  # Save the state vector after entangling qubits 0 and 1
qc.barrier()               # Add a barrier for clarity

# Perform a Hadamard on qubit 0
qc.h(0)        # Apply Hadamard on qubit 0 to create superposition in the 2-qubit entangled system
state_3 = Statevector(qc)  # Save the state vector after applying Hadamard
qc.barrier()               # Barrier to separate this section

# Apply further entangling gates between qubits
qc.cx(0, 2)    # Apply CNOT with qubit 0 as control and qubit 2 as target
qc.cz(1, 2)    # Apply CZ gate with qubit 1 as control and qubit 2 as target

# Measurement of qubits 0 and 1 and storing results in classical bits
qc.measure(0, 0)  # Measure qubit 0 and store result in classical bit 0
qc.measure(1, 1)  # Measure qubit 1 and store result in classical bit 1

# Bob applies conditional gates based on the measurement results
qc.z(2).c_if(qc.clbits[0], 1)  # Apply Z gate to qubit 2 if classical bit 0 is 1
qc.x(2).c_if(qc.clbits[1], 1)  # Apply X gate to qubit 2 if classical bit 1 is 1

# Draw the quantum circuit
qc.draw(output='mpl')

# Running the simulation
qc.save_statevector()                     # Save the final state vector of the circuit
sim = Aer.get_backend('aer_simulator')    # Get the Qiskit Aer simulator backend
res = sim.run(qc, shots=1024).result()    # Run the circuit on the simulator with 1024 shots

# Get the final state after simulation
final_state = res.get_statevector(qc)

# Plot the Bloch sphere of the final state
plot_bloch_multivector(final_state)
