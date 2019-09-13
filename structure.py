import numpy as np

# Import Qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute
from qiskit.tools.visualization import plot_state_city

from qiskit.providers.aer import StatevectorSimulator



# Code to apply a particular gate


def apply_operation(state_vector, qc_op):
    # state vector is an array of four complex numbers
    # qc_op is a QuantumCircuit object corresponding to the operation

    # Initialize an empty quantum circuit with the state vector
    circ0 = QuantumCircuit(2)
    circ0.initialize(state_vector, [0,1])

    # append the qc from the argument
    circ=circ0+qc_op

    # User the Aer StatevectorSimulator to comput the result
    simulator = Aer.get_backend('statevector_simulator')
    result = execute(circ, simulator).result()
    return  result.get_statevector(circ);


# QC implementing a particular operator the player can use
qc_h1 = QuantumCircuit(2)
qc_h1.h(0)

qc_x1 = QuantumCircuit(2)
qc_x1.x(0)


statevector= [ 1, 0, 0, 0]

statevector = apply_operation(statevector, qc_x1)
print(statevector)

statevector = apply_operation(statevector, qc_h1)
print(statevector)
