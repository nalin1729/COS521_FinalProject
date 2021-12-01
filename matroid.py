import random
import itertools
import math

from numpy.matrixlib.defmatrix import matrix

class Matroid:
    # Elements are always assumed to be 0, 1, ..., n - 1
    # IMPORTANT: ind_sets must be a set of frozensets
    def __init__(self, n, ind_sets):
        self.n = n
        self.I = ind_sets

    def __str__(self):
        return f"Matroid([{str(sorted([list(s) for s in self.I], key=lambda s: (len(s), s)))[1:-1].replace('[', '{').replace(']', '}')}])"

    def is_independent(self, s):
        return s in self.I

    # Finds a max-weight basis of given set of elements (that is a subset of 0, ..., n - 1)
    # Here elements is a dictionary where the key is element index and value is weight
    def find_max_weight_basis(self, elements):
        # Use the greedy algorithm
        order = sorted(elements.items(), key=lambda item: item[1], reverse=True)
        weight = 0
        
        current = frozenset()
        for e in order:
            potential = current.union(frozenset([e[0]]))
            if self.is_independent(potential):
                current = potential
                weight += e[1]

        return weight, current

    # Return all elements in the span of the given elements
    def span(self, elements):
        elements_with_weights = dict([(e, 0) for e in elements])
        basis = self.find_max_weight_basis(elements_with_weights)[1]

        # brute force: loop through all elements and check if spanned by basis
        span = set()
        for i in range(self.n):
            if i in basis: span.add(i)
            else:
                if not self.is_independent(basis.union(frozenset([i]))): span.add(i)

        return span

class VectorMatroid(Matroid):
    def __init__(self, vectors):
        self.n = len(vectors)
        self.matrix = vectors
        self.index_to_vector = {}
        for i, vector in enumerate(vectors):
            self.index_to_vector[vector] = i

    def __str__(self):
        return str(matrix)

    def is_independent(self, s):
        from numpy.linalg import matrix_rank

        s = tuple([self.matrix[e] for e in s])
        return matrix_rank(s) == len(s)

    # Same interface as Matroid
    def find_max_weight_basis(self, elements):
        return super().find_max_weight_basis(elements)

    # Same interface as Matroid
    def span(self, elements):
        #print(elements)
        return super().span(elements)

def random_matroid(n, rank, num_bases):
    assert num_bases <= math.comb(n, rank), 'number of bases must be at most nCr(n, rank)'
    assert rank <= n, 'rank cannot exceed n'
    assert rank * num_bases >= n, 'rank * num_bases must exceed n to fill the universe'

    # select num_bases randomly
    bases = random.sample(list(itertools.combinations(range(n), rank)), num_bases)
    universe = set()
    for b in bases: universe = universe.union(set(b))
    while len(universe) < n:
        bases = random.sample(list(itertools.combinations(range(n), rank)), num_bases)
        universe = set()
        for b in bases: universe = universe.union(set(b))

    # generate all subsets of all bases, could maybe be made more efficient
    ind_sets = set(frozenset(x) for b in bases for i in range(1, rank+1) for x in itertools.combinations(b, i))
    return Matroid(n, ind_sets)

if __name__ == '__main__':
    # random.seed(192)
    # M = random_matroid(7, 3, 3)
    # print(M)

    # print(M.find_max_weight_basis({2: 3, 1: 5, 4: 3, 6: 10, 3: 2}))

    vectors = ((1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12), (-4, 3, 2))
    M = VectorMatroid(vectors)
    print(M.span((3,2)))

