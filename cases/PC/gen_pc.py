import random


def case():

    # Setup
    delegates = random.randint(1, 1_000)
    ops = random.randint(1, 100_000)
    print(delegates, ops)

    # Set up some relations
    setup = ops // 2
    ops -= setup
    for _ in range(setup):
        op = random.randint(1, 2)
        X = random.randint(1, delegates - 1)  # so we can always add 1
        Y = random.randint(1, delegates)
        if X == Y:
            X += 1
        print(op, X, Y)

    # Operations
    for _ in range(ops):
        op = random.randint(1, 4)
        X = random.randint(1, delegates - 1)
        Y = random.randint(1, delegates)
        if X == Y:
            X += 1
        print(op, X, Y)


def test():
    N = random.randint(1, 100)
    print(N)

    for _ in range(N):
        case()


test()
