import bisect
import itertools as it

def gen_primes():
    """Infinitely generate primes"""
    yield from (2, 3, 5)
    composites = { 9: 3, 25: 5 }
    cycler = it.cycle((1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0))
    modulos = frozenset((1, 7, 11, 13, 17, 19, 23, 29))
    for odd_num in it.compress(
            it.islice(it.count(7), 0, None, 2),
            cycler):
        
        prime_factor = composites.pop(odd_num, None)
        if prime_factor is None:
            composites[odd_num*odd_num] = odd_num
            yield odd_num
        else:
            x = odd_num + 2*prime_factor
            while x in composites or (x%30) not in modulos:
                x += 2*prime_factor
            composites[x] = prime_factor
    return


class InfiniteSequence:
    def __init__(self, generating_function):
        self.gf = generating_function()
        self.cache = [next(self.gf)]

    def compute(self, n):
        """Extend the cache with primes up to n"""
        while self.cache[-1] < n:
            nxt = next(self.gf)
            self.cache.append(nxt)

    def below(self, upper):
        return self.between(2, upper)
            
    def between(self, lower, upper=None):
        """Primes are an increasing sequence, which we can use to speed up
        searching."""
        if upper is None:
            lower, upper = 2, lower
            
        self.compute(upper)
        i1 = bisect.bisect_left(self.cache, lower)
        i2 = bisect.bisect_left(self.cache, upper)
        return self.cache[i1:i2]
    
    def count_between(self, lower, upper=None):
        """How many primes exist below n"""
        if upper is None:
            lower, upper = 2, lower
        
        self.compute(upper)
        i1 =  bisect.bisect_left(self.cache, lower)
        i2 =  bisect.bisect_left(self.cache, upper)
        return i2 - i1
    
    def next_after(self, n):
        self.compute(n+1)
        i = bisect.bisect_right(self.cache, n)
        return self.cache[i]
    
Primes = InfiniteSequence(gen_primes)


if __name__ == '__main__':
    from datetime import datetime
    # N = 10_000
    # print(datetime.now())
    # q = Primes.between(13, 100)
    # print(q)
    
    # q = Primes.count_between(13, 97)
    # print(q)
    
    # q = Primes.next_after(110)/
    # print(q)