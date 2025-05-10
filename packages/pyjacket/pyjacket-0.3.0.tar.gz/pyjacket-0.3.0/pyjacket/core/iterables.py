from itertools import filterfalse, zip_longest
from typing import Iterable

"""Custom iterable methods"""
def partition(condition, iterable):
    """This should be a builtin at some point"""
    return (
        [*filter(     condition, iterable)],
        [*filterfalse(condition, iterable)],
    )
    
"""Custom filters"""
def exclude_filter(a, exclude=None):
    return filter(lambda x: x != exclude, a)


"""Indexing"""
def index_nth(iterable: list, element, n: int=-1) -> int:
    """Find nth (default: last) occurence of element in iterable."""    
    if n == 0:
        raise ValueError(f"n must be nonzero")

    if n < 0:  
        idx = len(iterable) - index_nth(iterable[::-1], element, -n) - 1
    
    else:
        idx = iterable.index(element)
        while idx >= 0 and n > 1:
            idx = iterable.index(element, idx+1)
            n -= 1
            
    return idx


"""Custom iterators"""
def circular_permutations(arr):
    for i in range(len(arr)):
        yield arr[i:] + arr[:i]
        
def batched(iterable, n):
    """Expects iterable length to be multiple of input"""
    N = len(iterable)
    for i in range(0, N, n):
        yield iterable[i:i+n] 

def batched(iterable: Iterable, batch_size: int, fill_value = None):
    """
    Yield successive batches from the iterable.

    Args:
        iterable: An iterable to batch.
        batch_size: The size of each batch.
        fill_value: The value to fill in for incomplete batches.

    Yields:
        Lists containing the batches of specified size.
    """
    if batch_size <= 0:
        raise ValueError("Batch size must be greater than zero.")

    it = iter(iterable)
    return zip_longest(*[it] * batch_size, fillvalue=fill_value)
            
# def zipped(iterable, n):
#     N = len(iterable)
#     for i in range(0, N):
#         yield iterable[i: i+n]

"""Element rearrangements"""
def sortby(X, Y):
    return [x for (y,x) in sorted(zip(Y,X), key=lambda pair: pair[0])] 

def zipped(iterable, n):
    iterable = iter(iterable)
    v = tuple(next(iterable) for _ in range(n))
    yield v
    for e in iterable:
        v = (*v[1:], e)
        yield v       
        
        
        
        
        
        



    