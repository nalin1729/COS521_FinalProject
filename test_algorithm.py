import random

# Import any algorithm implementations here

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

    # Finds the max-weight basis of given set of elements (that is a subset of 0, ..., n - 1)
    # Here elements is a dictionary where the key is element index and value is weight
    def find_max_weight_basis(self, elements):
        order = sorted(elements.items(), key=lambda item: item[1])

        current = frozenset()
        for e in order:
            potential = current.union(frozenset([e[0]]))
            if self.is_independent(potential):
                current = potential

        return current

    # Return all elements in the span of the given elements
    def span(self, elements):
        basis = self.find_max_weight_basis(elements)

        span = set()
        for i in range(self.n):
            if i in basis: span.add(i)
            else:
                if not self.is_independent(basis.union(frozenset(i))): span.add(i)

        return span

class FreeOrderMatroidAlgo:
    def __init__(self, matroid):
        self.matroid = matroid

    # Return the index of the next item that the algorithm wants. Must never
    # re-request an item
    def next_request(self):
        pass

    # Return whether or not the algorithm is accepting this item
    def accept(self, item, weight):
        pass

# algo is assumed to be a FreeOrderMatroidAlgo. Returns averaged payoff over all trials
# weights will be a list of values of each item
def run_trials(num_trials, algo, matroid, weights):
    sum = 0
    for i in range(num_trials):
        for _ in range(matroid.n):
            item = algo.next_request()
            sum += weights[item] * algo.accept(item, weights[item])

    return sum / num_trials

class Conjecture(FreeOrderMatroidAlgo):
    def __init__(self, matroid):
        super().__init__(matroid)

        self.i = 0 # For iteration over P
        
        # Sample S
        S = set()
        for i in range(self.n):
            if random.rand() < 0.5: S.add(i)
        S = frozenset(S)
        self.X = self.matroid.find_max_weight_basis(S) # max-weight basis of S

        self.current_iteration = 0

    def next_request(self):
        pass
