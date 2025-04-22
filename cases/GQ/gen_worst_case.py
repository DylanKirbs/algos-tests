import random

NUM_TEST_CASES = 20
K = 5000
M = 100000
W = 100000
Q = 100000
D = 100000

print(NUM_TEST_CASES)

for _ in range(NUM_TEST_CASES):
    print(f"{K} {M}")

    # --- Vertex weights ---
    for _ in range(K):
        print(random.randint(-10000, 10000))

    # --- Unique edges ---
    edges = set()
    while len(edges) < M:
        u = random.randint(1, K - 1)
        v = random.randint(u + 1, K)
        edges.add((u, v))

    edges = list(edges)
    random.shuffle(edges)

    for u, v in edges:
        print(f"{u} {v}")

    # --- Phase 1: Weight Updates ---
    for _ in range(W):
        node = random.randint(1, K)
        new_weight = random.randint(-10000, 10000)
        print(f"1 {node} {new_weight}")

    # --- Phase 2: Queries ---
    for _ in range(Q):
        x = random.randint(1, K)
        y = random.randint(1, min(K, 50))
        print(f"2 {x} {y}")

    # --- Phase 3: Deletions ---
    edge_ids = list(range(1, D + 1))
    random.shuffle(edge_ids)
    for eid in edge_ids:
        print(f"0 {eid}")

    # Final guaranteed query (per spec)
    print("2 1 1")

    # End of test case
    print("3")
