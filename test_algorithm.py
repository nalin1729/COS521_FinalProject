import random
from collections import defaultdict
from matroid import random_matroid

# Import any algorithm implementations here

class FreeOrderMatroidAlgo:
    def __init__(self, matroid, weights):
        assert matroid.n == len(weights)

        self.matroid = matroid
        self.weights = weights

class Conjecture(FreeOrderMatroidAlgo):
    def __init__(self, matroid, weights):
        super().__init__(matroid, weights)
        
        # Sample S
        S = []
        self.P = set()
        for i in range(self.matroid.n):
            if random.random() < 0.5: 
                S.append((i, self.weights[i]))
            else: self.P.add(i)

        self.P = frozenset(self.P)
        self.X = self.matroid.find_max_weight_basis(dict(S)) # max-weight basis of S

        self.current_iteration = 0
        self.current_span = frozenset()

    def run_trial(self):
        total = 0
        remaining = set([i for i in range(self.matroid.n)]) # which elements haven't been seen yet
        current_span = frozenset()
        A = frozenset() # store the answer

        for i, basis_elem in enumerate(self.X):
            next_span = self.matroid.span(self.X[:i + 1]).intersection(self.P)
            candidates = list(next_span.difference(current_span))
            random.shuffle(candidates)

            for y in candidates:
                remaining.remove(y)
                if self.weights[y] > self.weights[basis_elem]:
                    if self.matroid.is_independent(A.union(frozenset([y]))): 
                        A = A.union(frozenset([y]))
                        total += self.weights[y]

            current_span = next_span

        remaining = list(remaining)
        random.shuffle(remaining)
        for y in remaining:
            if self.matroid.is_independent(A.union(frozenset([y]))): 
                A = A.union(frozenset([y]))
                total += self.weights[y]

        return total, A

# algo is assumed to be a FreeOrderMatroidAlgo. Returns averaged payoff over all trials
# weights will be a list of values of each item
def run_trials(num_trials, matroid, weights):
    sum = 0
    total_counts = defaultdict(lambda: 0)
    for _ in range(num_trials):
        algo = Conjecture(matroid, weights)
        weight, included = algo.run_trial()
        sum += weight

        for element in included: total_counts[element] += 1

    return sum / num_trials, total_counts

if __name__ == '__main__':
    random.seed(192)
    n = 7; rank = 3; numBases = 3
    M = random_matroid(n, rank, numBases)
    print(M)

    # print(M.find_max_weight_basis({2: 3, 1: 5, 4: 3, 6: 10, 3: 2}))
    # print(M.span([2, 4]))

    weights = [random.randint(0, 10) for i in range(n)]
    print(weights)
    print(run_trials(100, M, weights))
    print(M.find_max_weight_basis(dict([(i, weight) for i, weight in enumerate(weights)])))