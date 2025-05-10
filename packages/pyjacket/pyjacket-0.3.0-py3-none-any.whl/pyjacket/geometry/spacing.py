"""Calculate how much spacing there is between """

# x--...--x
def space_between(L: float, n: int):
    if n < 2:  raise ValueError("Spacing requires more than one point")
    return L / (n-1)

# -x--...--x-
def space_evenly(L: float, n: int):
    if n < 2:  raise ValueError("Spacing requires more than one point")
    return L / (n+0)

# --x--...--x--
def space_around(L: float, n: int):
    if n < 2:  raise ValueError("Spacing requires more than one point")
    return L / (n+1)
