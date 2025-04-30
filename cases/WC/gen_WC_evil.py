#!/usr/bin/env python3

import random
import string

def make_low_entropy_word(length=15):
    patterns = ["a", "b", "ab", "aa", "bb", "aba", "bab"]
    pattern = random.choice(patterns)
    word = (pattern * ((length // len(pattern)) + 1))[:length]
    return word

def slightly_mutate(word):
    i = random.randint(0, len(word) - 1)
    c = random.choice(string.ascii_lowercase)
    return word[:i] + c + word[i+1:]

def generate_worst_overlap_case(num_words=20, word_len=15):
    words = set()
    tries = 0
    max_tries = 500

    while len(words) < num_words:
        word = make_low_entropy_word(word_len)
        if word not in words:
            words.add(word)
            tries = 0
        else:
            # Try a few mutations to increase uniqueness
            mutated = slightly_mutate(word)
            if mutated not in words:
                words.add(mutated)
                tries = 0
            else:
                tries += 1
                if tries > max_tries:
                    raise RuntimeError("Could not generate enough unique low-entropy words.")
    return list(words)

def generate_all_cases(num_cases=20):
    print(num_cases)
    for _ in range(num_cases):
        words = generate_worst_overlap_case()
        print(len(words))
        for word in words:
            print(word)

if __name__ == "__main__":
    generate_all_cases()
