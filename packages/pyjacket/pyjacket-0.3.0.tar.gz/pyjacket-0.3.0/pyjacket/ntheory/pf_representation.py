
from math import prod
from itertools import product

class Number:

    def __init__(self, pf: dict):
        self.pf = pf
        self._value = None

    @property
    def value(self):
        if self._value is None:
            print('heavy lifting')
            self._value = prod([k**v for k, v in self.pf.items()])
        return self._value
    
    def factors(self):
        # iterate through the coefficients in increasing order



        coefs = product(*[range(v//2+1) for v in self.pf.values()])
        next(coefs)
        for coef in coefs:
            print(coef)
            f1 = {p: c for p, c in zip(self.pf, coef)}
            # f2 = {p: n - c for (p, n), c in zip(self.pf.items(), coef)}
            yield Number(f1)
            # if f1 != f2:
            #     yield Number(f2)


# 2^0 3^0 x 2^2 3^1 = n
# 2^1 3^0 x 2^1 3^1 = n
# 2^0 3^1 x 2^2 3^0 = n

# 12 /
#  2  (6)
#  3  (4)






    def __mul__(self, other):
        pf = self.pf.copy()
        for k, v in other.pf.items():
            pf[k] = pf.get(k, 0) + v
        return Number(pf)
    
    def __repr__(self):
        return f"Num({self.pf})"
    






twelve = Number({2:2, 3:1})


thirteen = Number({13:1})

print(twelve)
print(twelve)

q = twelve * thirteen
print(q)

for f in twelve.factors():
    print(f, f.value)
















"""

3^1     7^1

3^2
















"""