from math import isqrt


def prime_factors(n):
    factors = {}
    # Divide n by 2 until it's odd
    while n % 2 == 0:
        if 2 in factors:
            factors[2] += 1
        else:
            factors[2] = 1
        n //= 2
    
    # Now n is odd, so we only need to check odd numbers up to sqrt(n)
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            if i in factors:
                factors[i] += 1
            else:
                factors[i] = 1
            n //= i
    
    # If n is a prime greater than 2
    if n > 2:
        factors[n] = 1
    
    return factors

def factors(n):
    prime_factorization = prime_factors(n)
    primes = list(prime_factorization.keys())
    powers = list(prime_factorization.values())
    num_primes = len(primes)
    factors_list = []
    for i in range(2 ** num_primes):
        factor = 1
        for j in range(num_primes):
            if (i >> j) & 1:
                factor *= primes[j] ** powers[j]
        factors_list.append(factor)
    factors_list.sort()
    return factors_list

def factors(n):
    prime_factorization = prime_factors(isqrt(n))
    factors_list = [1]
    for prime, power in prime_factorization.items():
        new_factors = []
        for factor in factors_list:
            for _ in range(power):
                factor *= prime
                new_factors.append(factor)
                # new_factors.append(n//factor)
                print(factor, n//factor)
        factors_list.extend(new_factors)
    return sorted(factors_list)

# Example usage:
n = 3600
print("Factors of", n, "are:", factors(n))