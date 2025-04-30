#!/usr/bin/env python3

import random
import string

def generate_overlap_words(num_words=20, word_len=15, base_len=500):
    base = ''.join(random.choices(string.ascii_lowercase, k=base_len))
    words = set()
    step = max(1, (base_len - word_len) // (num_words + 5))

    i = 0
    while len(words) < num_words and i + word_len <= len(base):
        word = base[i:i + word_len]
        if len(word) >= 3:
            words.add(word)
        i += random.randint(1, step)

    if len(words) < num_words:
        raise RuntimeError("Failed to generate enough overlapping words.")

    return list(words)

def generate_stress_case(num_cases=100, words_per_case=20):
    print(num_cases)
    for _ in range(num_cases):
        words = generate_overlap_words(words_per_case)
        print(len(words))
        for word in words:
            print(word)

if __name__ == "__main__":
    generate_stress_case()
