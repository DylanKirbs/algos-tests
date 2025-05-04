#!/usr/bin/env python3

import random

def generate_test_case():
    X = random.randint(1, 250)
    Y = random.randint(1, 250)
    max_H = min(X * Y * 2, 5000)  # allow multiple houses per cell
    H = random.randint(2, max_H)
    K = random.randint(1, H // 2)

    houses = []
    for _ in range(H):
        x = random.randint(0, X - 1)
        y = random.randint(0, Y - 1)
        houses.append((x, y))

    return (X, Y, H, K, houses)

def main():
    N = random.randint(1, 100)
    print(N)
    for _ in range(N):
        X, Y, H, K, houses = generate_test_case()
        print(f"{X} {Y}")
        print(f"{H} {K}")
        for x, y in houses:
            print(f"{x} {y}")

if __name__ == "__main__":
    main()
