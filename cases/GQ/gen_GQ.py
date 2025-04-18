import random
from itertools import combinations


def case():

    # Setup
    K = random.randint(1, 20_000)
    M = random.randint(0, 100_000)
    print(K, M)

    # Vert weights
    for _ in range(K):
        W = random.randint(-10_000, 10_000)
        print(W)

    # Edges
    edges = set()
    for _ in range(M):
        # unique edges
        D = random.randint(1, K)
        E = random.randint(1, K)
        while D == E or (D, E) in edges or (E, D) in edges:
            D = random.randint(1, K)
            E = random.randint(1, K)
        print(D, E)
        edges.add((D, E))

    # Operations
    for _ in range(random.randint(2000, 2000)):
        op = random.randint(0, 15)
        # 0   Delete
        # 1-5 Weight
        # 6-15 Query
        if op == 0:
            # Delete edge
            X = random.randint(1, M)
            print(0, X)
        elif op <= 5:
            # Change weight
            X = random.randint(1, K)
            Y = random.randint(-10_000, 10_000)
            print(1, X, Y)
        else:
            # Query
            X = random.randint(1, K)
            Y = random.randint(1, K)
            print(2, X, Y)

    print(3)  # terminate case


def test():
    N = random.randint(1, 20)
    print(N)

    for _ in range(N):
        case()


test()
