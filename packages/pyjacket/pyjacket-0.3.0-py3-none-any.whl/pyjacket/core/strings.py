
from typing import Union

def truncate(s: str, n: int, symbol=''):
    """Fixes the length of a string. Use truncation symbol <symbol> to denote truncation."""

def truncate_modulo(s: str, mod: int):
    """Ensures length of a string <s> is a multiple of <n>"""
    r = len(s) % mod
    if r: s = s[:-r]
    return s

def extend(): ...

def extend_modulo(s: str, n:int, fillval='0'):
    """Pads a fill value to ensure len(s) is a multiple of n"""
    if len(fillval) != 1: raise ValueError('fillvalue must be a single character')
    s += fillval * (-len(s) % n)
    return s

def isplit(s: str, i: Union[int, list[int]]):
    """split a string at index or list of indices"""
    if isinstance(i, int):
        i = [i]
    
    i.sort()
    return [s[i1:i2] for i1, i2 in zip([None]+i, i+[None])]



if __name__ == '__main__':
    s = 'Hello there mate'
    n = 6
    q = truncate_modulo(s, n)
    print(q)


    s = 'abcdefghijkl'
    i = 8
    q = isplit(s, i)
    print(q)