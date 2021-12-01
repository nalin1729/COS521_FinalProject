import random
import itertools
import math
from test_algorithm import Matroid

def random_matriod(n, rank, num_bases):
    assert num_bases <= math.comb(n, rank), 'number of bases must be at most nCr(n, rank)'
    assert rank <= n, 'rank cannot exceed n'

    universe = list(range(n))
    all_bases = itertools.combinations(universe, rank)
    random.shuffle(universe)

    # select num_bases randomly
    indices = set(universe[:num_bases])
    bases = set()
    for i, b in enumerate(all_bases):
        if i in indices: bases.add(frozenset(b)) 

    # generate all subsets of all bases, could maybe be made more efficient
    ind_sets = set(frozenset(x) for b in bases for i in range(1, rank+1) for x in itertools.combinations(b, i))
    return Matroid(n, ind_sets)

if __name__ == '__main__':
    M = random_matriod(5, 3, 3)
    print(M)
