import random
import itertools
import math
from test_algorithm import Matroid

def random_matriod(n, rank, num_bases):
    max_bases = math.comb(n, rank)
    assert num_bases <= max_bases, 'number of bases must be at most nCr(n, rank)'
    assert rank <= n, 'rank cannot exceed n'

    all_bases = itertools.combinations(range(n), rank)
    bases_indices = random.sample(range(max_bases), num_bases)

    # select num_bases randomly
    bases = set()
    for i, b in enumerate(all_bases):
        if i in bases_indices: bases.add(frozenset(b)) 

    # generate all subsets of all bases, could maybe be made more efficient
    ind_sets = set(frozenset(x) for b in bases for i in range(1, rank+1) for x in itertools.combinations(b, i))
    return Matroid(n, ind_sets)

if __name__ == '__main__':
    M = random_matriod(5, 3, 3)
    print(M)
