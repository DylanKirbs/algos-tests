import random

def generate_fingerprint():
    M = random.randint(0, 100)
    F = [random.randint(0, 255) for _ in range(M)]
    return f"{M} " + " ".join(map(str, F))

def generate_test_cases(num_cases):
    output = [str(num_cases)]
    
    for _ in range(num_cases):
        # K and T
        K = random.randint(0, 20)
        T = random.randint(0, 255)
        output.append(f"{K} {T}")

        # Existing documents
        E = random.randint(0, 50)
        output.append(str(E))
        for _ in range(E):
            output.append(generate_fingerprint())

        # Candidate documents
        C = random.randint(1, 50)
        output.append(str(C))
        for _ in range(C):
            output.append(generate_fingerprint())

    return "\n".join(output)

# Example usage
if __name__ == "__main__":
    num_cases = random.randint(1, 100)
    test_data = generate_test_cases(num_cases)
    print(test_data)
