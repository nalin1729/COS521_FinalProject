import random
from collections import defaultdict

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
        # Use the greedy algorithm
        order = sorted(elements.items(), key=lambda item: item[1], reverse=True)
        
        current = frozenset()
        for e in order:
            potential = current.union(frozenset([e[0]]))
            print(potential)
            if self.is_independent(potential):
                current = potential

        return current

    # Return all elements in the span of the given elements
    def span(self, elements):
        elements_with_weights = dict([(e, 0) for e in elements])
        basis = self.find_max_weight_basis(elements_with_weights)

        # brute force: loop through all elements and check if spanned by basis
        span = set()
        for i in range(self.n):
            if i in basis: span.add(i)
            else:
                if not self.is_independent(basis.union(frozenset(i))): span.add(i)

        return span

class FreeOrderMatroidAlgo:
    def __init__(self, matroid, weights):
        assert matroid.n == len(weights)

        self.matroid = matroid
        self.weights = weights

# algo is assumed to be a FreeOrderMatroidAlgo. Returns averaged payoff over all trials
# weights will be a list of values of each item
def run_trials(num_trials, algo):
    sum = 0
    total_counts = defaultdict(lambda: 0)
    for i in range(num_trials):
        weight, included = algo.run_trial()
        sum += weight

        for element in included: total_counts[element] += 1

    return sum / num_trials, total_counts

class Conjecture(FreeOrderMatroidAlgo):
    def __init__(self, matroid):
        super().__init__(matroid)
        
        # Sample S
        S = set()
        self.P = set()
        for i in range(self.n):
            if random.rand() < 0.5: S.add(i)
            else: self.P.add(i)
        S = frozenset(S)
        self.P = frozenset(self.P)
        self.X = self.matroid.find_max_weight_basis(S) # max-weight basis of S

        self.current_iteration = 0
        self.current_span = frozenset()

    def run_trial(self):
        total = 0
        remaining = set([i for i in range(self.matroid.n)]) # which elements haven't been seen yet
        current_span = frozenset()
        A = frozenset() # store the answer

        for i, basis_elem in enumerate(self.X):
            next_span = self.matroid.span(self.X[:i + 1]).intersect(self.P)
            candidates = random.shuffle(list(next_span.difference(current_span)))

            for y in candidates:
                remaining.remove(y)
                if self.weights[y] > self.weights[basis_elem]:
                    if self.matroid.is_independent(A.union(frozenset([y]))): 
                        A = A.union(frozenset([y]))
                        total += self.weights[y]

        for y in random.shuffle(list(remaining)):
            if self.matroid.is_independent(A.union(frozenset([y]))): 
                A = A.union(frozenset([y]))
                total += self.weights[y]

        return total, A
