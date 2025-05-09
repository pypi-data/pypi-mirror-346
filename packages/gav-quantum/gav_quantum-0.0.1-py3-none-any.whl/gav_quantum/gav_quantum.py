import numpy as np


ZERO = np.array([1, 0])
ONE = np.array([0,1])
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j],[1j, 0]])
Z = np.array([[1, 0], [0, -1]])
PAULIS = np.array([np.eye(2), X, Y, Z])


def bell_states():
    bell_states = {
        'PHI_PLUS': np.kron(ZERO, ZERO) + np.kron(ONE, ONE),
        'PHI_MINUS': np.kron(ZERO, ZERO) - np.kron(ONE, ONE),
        'PSI_PLUS': np.kron(ZERO, ONE) + np.kron(ONE, ZERO),
        'PSI_MINUS': np.kron(ZERO, ONE) - np.kron(ONE, ZERO)
    }
    bell_states = {k: v * 1/np.sqrt(2) for k, v in bell_states.items()}
    return bell_states
BELL_STATES = bell_states()


# Returns W-state of N qubits
def W(N):
    ret_state = np.zeros(2**N)
    for basis in np.identity(N):
        for index, entry in enumerate(basis):
            state = ZERO if entry == 0 else ONE
            if(index == 0):
                kron_state = ZERO if entry == 0 else ONE
            else:
                kron_state = np.kron(kron_state, state)

        ret_state += kron_state
    return ret_state/ np.sqrt(N)


# Returns GHZ-state of N qubits
def GHZ(N):
    ret_state = np.zeros(2**N)
    ret_state[0] = ret_state[-1] = 1
    return ret_state / np.sqrt(2)


# Returns the operator specified via tensor notation
# INPUTS
#     N - Number of qubits
#     nonidentities - List of tuples specifying qubit number (indexed at 0) in ascending order and Pauli operator.  
#         Example: [(0,X),(2,'Y')]
def operator_from_sparse_pauli(N, nonidentities):
    tup = lambda value, tuples: next(((first, second) for first, second in tuples if first == value), 0)
    
    for iter in range(N):
        result = tup(iter, nonidentities)
        if(iter == 0):
            ret_arr = np.identity(2) if (result == 0) else result[1]
        else:
            ret_arr = np.kron(ret_arr, np.identity(2)) if result == 0 else np.kron(ret_arr, result[1])

    return ret_arr