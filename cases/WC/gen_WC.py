#!/usr/bin/env python3

import random
import string

def generate_test_case(num_words, min_len=3, max_len=15):
    alphabet = string.ascii_lowercase
    long_string = ''.join(random.choices(alphabet, k=200 + num_words * max_len))

    words = set()
    attempts = 0
    max_attempts = 1000

    while len(words) < num_words and attempts < max_attempts:
        start = random.randint(0, len(long_string) - max_len - 1)
        end = start + random.randint(min_len, max_len)
        word = long_string[start:end]
        if len(word) >= min_len and word not in words:
            words.add(word)
        attempts += 1

    if len(words) < num_words:
        raise ValueError("Could not generate enough unique words with overlaps.")

    return list(words)

def generate_cases():
    num_cases = random.randint(1, 100)
    print(num_cases)
    for _ in range(num_cases):
        words_per_case = random.randint(1, 20)
        words = generate_test_case(words_per_case)
        print(len(words))
        for word in words:
            print(word)

if __name__ == "__main__":
    generate_cases()
