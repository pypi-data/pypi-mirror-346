import numpy as np
from math import isqrt, prod

def primes_below(n) -> list:
    """Prime sieve"""
    if n <= 2:  return []
    if n == 3:  return [2]
    sieve = np.ones(n//3 + (n % 6 == 2), dtype=np.bool_)
    sieve[0] = False
    for i in range(isqrt(n)//3 + 1):
        if sieve[i]:
            k = 3*i+1 | 1
            sieve[((k*k)//3)::2*k] = False
            sieve[(k*k+4*k-2*k*(i & 1))//3::2*k] = False
    primes = (3*np.nonzero(sieve)[0]+1) | 1
    return [2, 3, *primes]

def prime_factors(n: int) -> dict:
    """Get the full prime factorization of a number"""
    factors = dict()
    for i in primes_below(isqrt(n)):
        while not n % i:
            factors[i] = factors.get(i, 0) + 1
            n //= i
    if n > 1:
        factors[n] = factors.get(n, 0) + 1  
    return factors

def is_prime(n: int) -> bool:
    """True if n is prime"""
    if n <= 1:  return False
    if n == 2:  return True
    for p in primes_below(isqrt(n) + 1):
        if not n%p:  return False
    return True

def phi(n: int | dict) -> int:
    """Count numbers coprime to (and below) n.
    Euler's Totient function.
    """
    factors = n if isinstance(n, dict) else prime_factors(n)
    r = 1
    for p, k in factors.items():
        r *= p**(k-1) * (p-1)
    return r

def congruent(a, b, modulo) -> bool:
    return (a % modulo) == (b % modulo)

def modular_inverse(): ...

def chinese_remainder_theorem(remainders: list, moduli: list):
    """Solve a system of congruences, such as:
    x = 3   (mod 5)
    x = 1   (mod 7)
    x = 6   (mod 8)
    => find all values for x that satisfy this system
    """
    N = prod(moduli)
    nums = N // moduli
    inverses = [modular_inverse(num, modulo)
                for num, modulo in zip(nums, moduli)]
    x = sum(r*n*i for r, n, i in zip(remainders, nums, inverses)) % N
    return x, N



# def primes_below(n):
#     """Prime sieve"""
#     if n < 3:  return np.array([])
#     if n == 3: return np.array([3])
#     sieve = np.ones(n//3 + (n % 6 == 2), dtype=np.bool_)
#     sieve[0] = False
#     for i in range(isqrt(n)//3+1):
#         if sieve[i]:
#             k = 3*i+1 | 1
#             sieve[((k*k)//3)::2*k] = False
#             sieve[(k*k+4*k-2*k*(i & 1))//3::2*k] = False
#     return np.r_[2, 3, ((3*np.nonzero(sieve)[0]+1) | 1)]