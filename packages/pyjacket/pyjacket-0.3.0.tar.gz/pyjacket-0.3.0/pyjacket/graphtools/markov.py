import numpy as np


def is_transition_matrix(m):
    # all entries must be between 0 and 1 (inclusive)
    ... 


def is_regular(m: np.ndarray) -> bool:
    """Test if a matrix reaches an equilibrium
    Maybe, testing if eigenvalue of 1 exists could be quicker
    """
    n = m.shape[0]
    if 0 not in m:  return True
    for _ in range((n-1)**2):
        m = m @ m
        if 0 not in m:  return True
    return False




def state_probabilities(m: np.ndarray) -> np.ndarray:
    """The probability to be in each state after moving along the graph for a long time.

    m: transition matrix.
    """
    vals, vectors = np.linalg.eig(m.T)
    vals = vals.real
    vectors = vectors.real

    # find eigenvectors whose values equal 1
    for val, vector in zip(vals, vectors.T):
        if abs(val - 1)  < 1e6:
            break
    else:
        raise ValueError('This matrix does not have any equilibrium!') 

    # normalize eigenvector to have sum 1
    vector /= vector.sum()
    return vector

def n_step_transitions(transition_matrix, n):
    """Probability to go from state i to state j in n steps:
    
    matrix[i, j]
    """
    return np.linalg.matrix_power(transition_matrix, n)

def is_connected(m, i, j):
    '''Is there a path between the two states?'''
    ...

if __name__ == '__main__':

    A = np.array([
        [0, 1],
        [.4, .6],
    ])
    assert is_regular(A) == True

    A = np.array([
        [1, 0],
        [.3, .7],
    ])
    assert is_regular(A) == False

    A = np.array([
        [.1, .3, .6],
        [.6, .2, .2],
        [.1, .3, .6]
    ])
    assert np.all(state_probabilities(A).round(3) == np.array([0.236, 0.273, 0.491]))
