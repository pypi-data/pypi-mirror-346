N = 41

A = 13

B = 17

n = N.bit_length()

R = 0

for i in range(0, n):
    q = int(R + (A & (1 << i) != 0) * B) % 2
    R = int((R + (A & (1 << i) != 0) * B + q * N) / 2)

print("Result:", R % N, A*B % N)