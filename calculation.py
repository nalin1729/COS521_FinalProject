import math
from numpy import exp

n = 800
k = 332
p = 0.5

cterm = lambda j: math.comb(j - 2, k - 1) * (p ** k) * (1 - p) ** (j - k) * min(1, k / (j - k))
dterm = lambda j: math.comb(n, j) * (p ** j) * (1 - p) ** (n - j) * p * k / (n - j)

C = sum([cterm(j) for j in range(k + 1, n + 1)])
D = sum([dterm(j) for j in range(0, k + 1)])

print(C + D) 
