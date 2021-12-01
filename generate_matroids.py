import random
import itertools
import math
from test_algorithm import Matroid

def random_matroid(n, rank, num_bases):
    max_bases = math.comb(n, rank)
    assert num_bases <= max_bases, 'number of bases must be at most nCr(n, rank)'
    assert rank <= n, 'rank cannot exceed n'

    # select bases randomly
    bases = random.sample(list(itertools.combinations(range(n), rank)), num_bases) 

    # generate all subsets of all bases, could maybe be made more efficient
    ind_sets = set(frozenset(x) for b in bases for i in range(1, rank+1) for x in itertools.combinations(b, i))
    return Matroid(n, ind_sets)

if __name__ == '__main__':
    random.seed(192)
    M = random_matroid(7, 3, 3)
    print(M)

    print(M.find_max_weight_basis({2: 3, 1: 5, 4: 3, 6: 10, 3: 2}))
