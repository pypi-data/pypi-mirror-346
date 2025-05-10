"""Custom methods for integers"""



def digits(n: int, base: int=10):
    if not isinstance(n, int): raise ValueError(f'pyjacket.digits takes an integer, got {type(n)}')
    
    if base<=1: raise ValueError(f"Base must be greater than 1, got {base}")
    # elif base == 2: ...
    elif base == 10:  return [int(x) for x in str(n)]
    
    digits = []
    while n > 0:
        n, r = divmod(n, base)
        digits.insert(0, r)
    return digits




