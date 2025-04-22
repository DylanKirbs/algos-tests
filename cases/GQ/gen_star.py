import random

K = 20000
M = K - 1  # Star topology: node 1 connects to all others
W = 100000
Q = 100000
D = M

print("1")  # 1 test case
print(f"{K} {M}")

# --- Weights (random from spec range) ---
for _ in range(K):
    print(random.randint(-10000, 10000))

# --- Edges: node 1 connected to all others (star) ---
for i in range(2, K + 1):
    print(f"1 {i}")

# --- PHASE 1: 100k weight updates ---
for _ in range(W):
    node = random.randint(1, K)
    new_weight = random.randint(-10000, 10000)
    print(f"1 {node} {new_weight}")

# --- PHASE 2: 100k queries all on node 1 ---
# with varying Y from 1 to 20000 (or capped)
for i in range(Q):
    y = (i % K) + 1  # Cycles from 1 to K
    print(f"2 1 {y}")

# --- PHASE 3: randomised deletions ---
edge_ids = list(range(1, D + 1))
random.shuffle(edge_ids)
for eid in edge_ids:
    print(f"0 {eid}")

# Final guaranteed query (spec requirement)
print("2 1 1")

# End the test case
print("3")
