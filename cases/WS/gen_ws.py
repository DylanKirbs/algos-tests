import random
from itertools import combinations

DOWN_SCALING_FACTOR = 1


def case():
    K_num_towns = random.randint(1, 10_000 // DOWN_SCALING_FACTOR)
    D_num_dams = random.randint(1, K_num_towns)

    print(K_num_towns, D_num_dams)

    # The second line of each test case contains K
    # integers A1 A2 A3 . . . AK such that 0 ⩽ Ai ⩽ 1000i and Ai < A j when i < j;
    # the integers are separated by single spaces
    print(0, end="")
    prev = 0
    for i in range(1, K_num_towns):
        prev = random.randint(prev + 1, i * 1000 // DOWN_SCALING_FACTOR)
        print(f" {prev}", end="")
    print()


def test():
    N = random.randint(1, 100 // DOWN_SCALING_FACTOR)
    print(N)

    for _ in range(N):
        case()


test()
