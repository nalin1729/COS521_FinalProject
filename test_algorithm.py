import random
from collections import defaultdict
from matroid import VectorMatroid, random_matroid

# Import any algorithm implementations here

class FreeOrderMatroidAlgo:
    def __init__(self, matroid, weights):
        assert matroid.n == len(weights)

        self.matroid = matroid
        self.weights = weights

class Conjecture(FreeOrderMatroidAlgo):
    def __init__(self, matroid, weights, sample_prob):
        super().__init__(matroid, weights)
        
        # Sample S
        S = []
        self.P = set()
        for i in range(self.matroid.n):
            if random.random() < sample_prob: 
                S.append((i, self.weights[i]))
            else: self.P.add(i)

        self.P = frozenset(self.P)
        self.X = self.matroid.find_max_weight_basis(dict(S))[1] # max-weight basis of S
        self.X = sorted(list(self.X), key=lambda i: self.weights[i], reverse=True)

        self.current_iteration = 0
        self.current_span = frozenset()

    def run_trial(self):
        total = 0
        remaining = set(self.P) # which elements haven't been seen yet
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
        algo = Conjecture(matroid, weights, 0.36787944117)
        weight, included = algo.run_trial()
        sum += weight

        for element in included: total_counts[element] += 1

    for key in total_counts: total_counts[key] /= num_trials
    return sum / num_trials, total_counts

if __name__ == '__main__':
    random.seed(192)
    #n = 5; rank = 3; numBases = 3
    # M = random_matroid(n, rank, numBases)
    # print(M)

    # print(M.find_max_weight_basis({2: 3, 1: 5, 4: 3, 6: 10, 3: 2}))
    # print(M.span([2, 4]))

    vectors = ((1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12), (-4, 3, 2), (-5, -7, -8))
    n = len(vectors)
    M = VectorMatroid(vectors)
    weights = [random.randint(0, 10) for i in range(n)]
    print(weights)
    print(run_trials(1000, M, weights))
    print(M.find_max_weight_basis(dict([(i, weight) for i, weight in enumerate(weights)])))