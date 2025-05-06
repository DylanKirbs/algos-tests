import random
import sys

MAX_TERM_LENGTH = 200
MAX_TEST_CASES = 1000

def generate_safe_term():
    def gen(depth):
        if depth == 0 or random.random() < 0.3:
            return random.choice(['a', 'b', 'c', 'X', 'Y', 'Z'])
        head = random.choice('fgpq')
        arity = random.randint(1, 3)
        args = [gen(depth - 1) for _ in range(arity)]
        return f"({head} {' '.join(args)})"

    for _ in range(20):
        term = gen(random.randint(1, 5))
        if len(term) <= MAX_TERM_LENGTH:
            return term
    return 'a'

def write_test_cases():
    n = random.randint(10, MAX_TEST_CASES)
    print(n)
    for _ in range(n):
        while True:
            t1 = generate_safe_term()
            t2 = generate_safe_term()
            if len(t1) <= MAX_TERM_LENGTH and len(t2) <= MAX_TERM_LENGTH:
                print(f"{t1} {t2}")
                break

if __name__ == '__main__':
    write_test_cases()
