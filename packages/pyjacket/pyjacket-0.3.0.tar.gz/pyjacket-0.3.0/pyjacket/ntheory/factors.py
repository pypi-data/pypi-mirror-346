from functools import reduce
from math import isqrt
  
def factors(n):
    """return factors pairwise"""
    step = n%2 + 1
    return [[i, n//i] for i in range(1, isqrt(n)+1, step) if not n % i]

from itertools import product
def factors(pf: dict):
    coefs = product(*[range(v//2+1) for v in pf.values()])
    next(coefs)
    for coef in coefs:
        f1 = {p: c for p, c in zip(pf, coef)}
        f2 = {p: n - c for (p, n), c in zip(pf.items(), coef)}
        yield f1
        if f1 != f2:
            yield f2


for f in factors({11:3}):
    print(f)
# q = product(*[])
# q = list(q)
# print(q)


print('finished')
exit()





def divisors(n):
    """return factors pairwise"""
    step = n%2 + 1
    return sum(([i, n//i] for i in range(1, isqrt(n)+1, step) if not n % i), [])
    
    
    
    
def div_sum(n, proper=True):
    root = isqrt(n)
    r = -n if proper else 0
    if root * root == n:
        r -= root
    for x in range(1, root+1, n%2+1):
        if not n%x:
            r += x + n//x
    return r
    
        
        
        
# z = factors(124)

# print(z)