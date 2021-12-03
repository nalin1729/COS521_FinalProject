import random
#from matroid import Matroid

# https://www.sciencedirect.com/science/article/pii/0012365X75900758
def knuth_random_matroid(n):
    universe = frozenset(range(n))
    r = 0
    F = [set(frozenset())]
    while universe not in F[r]:
        # generate covers
        F_next = set(frozenset())
        if r == 0:
            for a in universe:
                F_next.add(frozenset([a]))
        else:
            for A in F[r]:
                for a in universe - A:
                    x = set(A)
                    x.add(a)
                    F_next.add(frozenset(x))

        # enlarge
        if r != 0:
            s = set(random.choice(list(F[r])))
            s = s.union(set(random.sample(list(universe-s), min(4, len(universe-s)))))
            F_next.add(frozenset(s))

        # test with n = 10 for example in paper
        # if r == 1:
        #     pi = [[1,3,4],[1,5,9],[2,5,6],[3,5,8],[3,7,9],[2,3,8]]
        #     for x in pi:
        #         F_next.add(frozenset(x))

        # superpose
        isContained = False
        while not isContained:
            isContained = True
            not_contained = []
            for A in F_next:
                for B in F_next:
                    if A == B: continue
                    if not contained(A.intersection(B), F[r]): 
                        not_contained.append((A, B))
                        isContained = False
            for AB in not_contained:
                A, B = AB
                if A in F_next and B in F_next:
                    F_next.remove(A)
                    F_next.remove(B)
                    F_next.add(A.union(B))
        F.append(F_next)
        r += 1
    
    closed_sets = []
    for rank, X in enumerate(F):
        for Y in X:
            closed_sets.append((rank, Y))

    Matroid(universe, circuit_closures = closed_sets)
    return closed_sets

def contained(AandB, Fr):
    if len(AandB) == 0: return True
    for C in Fr:
        if AandB.issubset(C): return True
    False

if __name__ == '__main__':
    knuth_random_matroid(10)