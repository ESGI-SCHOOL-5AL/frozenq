import numpy as np

# Import Qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute
from qiskit.tools.visualization import plot_state_city

from qiskit.providers.aer import StatevectorSimulator


from python_array import *

# Size of the gameboard -> nh,nw
nh = 2
nw = 2

#we need a dictionary
dict_states = ( [0,0,0,0],
                [1, 0, 0, 0], [0, 1, 0, 0],
                [1, 0, 0, 0], [1, 0, 0, 0], )

# QC implementing a particular operator the player can use
qc_h1 = QuantumCircuit(2)
qc_h1.h(0)

qc_x1 = QuantumCircuit(2)
qc_x1.x(0)

dicts_ops = (qc_h1, qc_x1, )

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

def find_match(state_vector):
    state_vector=np.conjugate(state_vector)
    for i in range(len(dict_states)):
        if np.abs( np.dot(state_vector,dict_states[i]) ) > 0.9:
            return i
        
    # if no match found, return the next integer
    return len(dict_states);

def shoot_state(state, row, column, State_array, Bubble_array):
    #### Input
    # state: np.array object describing the state vector shot
    # row, column: position where to apply it
    # State_array: array holding the quantum states at each location
    # Bubble_array: array holding the indices for the game-mechanics
    #### Returns
    # ( State_array, Bubble_array )

    State_array[row, column] = state;
    Bubble_array[row, column] = find_match(state);

    return find_clusters(Bubble_array, State_array);


def shoot_operator(qc_op, row, column, State_array, Bubble_array):
    #### Input
    # qc_op: QuantumCircuit object describing the operation to be done
    # column: column where to apply it
    # State_array: array holding the quantum states at each location
    # Bubble_array: array holding the indices for the game-mechanics
    #### Returns
    # ( State_array, Bubble_array)

    State_array[row, column] = apply_operation(State_array[row, column], qc_op)
    Bubble_array[row, column] = find_match(State_array[row, column]);
    
    return find_clusters(Bubble_array, State_array);

def debug_structure():


    State_array=np.zeros( (nh, nw, 4), dtype=complex)
    Bubble_array=np.full( (nh, nw, 4), np.nan)

    State_array[0,0]= np.array([ 1, 0, 0, 0])

    statevector = apply_operation(State_array[0,0], qc_x1)
    print(statevector)
    print(find_match(statevector))

    statevector = apply_operation(statevector, qc_h1)
    print(statevector)
    print(find_match(statevector))

    print(State_array)

# main
#debug_structure()
#debug_python_array()
