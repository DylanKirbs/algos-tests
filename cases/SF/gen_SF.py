import random
import string


def case():
    # Setup
    K = random.randint(4, 9)
    print(K)

    # Gen names
    for _ in range(K):
        length = random.randint(1, 15)
        random_name = (
                ''.join(random.choices(string.ascii_uppercase, k=1))
                + ''.join(random.choices(string.ascii_lowercase, k=length))
                + "_"
                + ''.join(random.choices(string.ascii_uppercase, k=1))
                + ''.join(random.choices(string.ascii_lowercase, k=length))
                + ".rec"
        )

        print(random_name)


def test():
    N = random.randint(10, 20)
    print(N)

    for _ in range(N):
        case()

test()
