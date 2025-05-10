import numpy as np

"""
rate: chance of occuring this timestep
prospect: chance of occuring eventually

absorbing state:  state whose only child is itself
transient state:  state with atleast one child other than itself

adjacent: connected in one step
connected: a path exists, which may be one or multiple steps
"""

def expected_visits(A: np.ndarray):
    """Expected number of visits to <j> - starting from <i> - before being absorbed."""
    I = np.identity(A.shape[0])
    return np.linalg.inv(I - A)


def is_absorbing(m: np.ndarray):
    """Is this matrix an absorbing matrix?"""
    # atleast one absorbing note exists
    # each transient state is connected to atleast one absorbing state
    ...


def classify_states(m):
    """Classify each state in a transition matrix as either absorbing or transient"""
    absorbing = []
    transient = []
    for i in range(m.shape[0]):
        if m[i, i] == 1:
            absorbing += [i]
        else:
            transient += [i]
    return transient, absorbing


def slice_absorbing(m: np.ndarray):
    """Spit matrix in components based on absorbing/transient"""
    transient, absorbing = classify_states(m)
    A = slice_cross(m, transient, absorbing)
    B = slice_cross(m, transient, transient)
    return A, B

def absorb_probabilities(m):
    """What is the probability to end in a particular absorbing state, starting from any transient state i"""
    A, B = slice_absorbing(m)
    F = expected_visits(B)
    return F @ A






if __name__ == '__main__':
    # Transition matrix
    # A = np.array([
    #     [0.2, 0.6, 0.2],
    #     [0.3, 0.0, 0.7],
    #     [0.5, 0.0, 0.5],
    # ]).T

    # A = np.array([
    #     [0.5, 0.2, 0.3],
    #     [0.6, 0.2, 0.2],
    #     [0.1, 0.8, 0.1],
    # ])

    # A = np.array([
    #     [2/3, 1/3, 0.0],
    #     [2/3, 0.0, 1/3],
    #     [2/3, 0.0, 0.0],
    # ])\


    # A = np.array([
    #     [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    #     [0.6, 0.0, 0.4, 0.0, 0.0, 0.0],
    #     [0.0, 0.6, 0.0, 0.4, 0.0, 0.0],
    #     [0.0, 0.0, 0.6, 0.0, 0.4, 0.0],
    #     [0.0, 0.0, 0.0, 0.6, 0.0, 0.4],
    #     [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    # ])


    A = np.array([
        [1, 0, 0, 0],
        [.7, 0, .3, 0],
        [.8, 0, 0, .2],
        [0, 0, 0, 1],
    ])


    def slice_cross(A, y, x):
        return A[y][:, x]



    # slice_absorbing(A)


    q = absorb_probabilities(A)

    # q = slice_cross(A, 2, 3)
    # print(q)


    # q = state_probabilities(A)


    # q = n_step_transitions(A, 2)[1, 0]


    # q = expected_visits(A) #[0, 2]

    # q = expected_visits(A)

    print(q)