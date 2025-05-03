import random

def generate_test_case(X, Y, H, K):
    lines = []
    lines.append(f"{X} {Y}")
    lines.append(f"{H} {K}")
    for _ in range(H):
        x = random.randint(0, X - 1)
        y = random.randint(0, Y - 1)
        lines.append(f"{x} {y}")
    return lines

def generate_input():
    MAX_TESTS = 100
    MAX_XY = 250
    MAX_H = 5000

    output_lines = [str(MAX_TESTS)]
    
    for _ in range(MAX_TESTS):
        X = MAX_XY
        Y = MAX_XY
        H = MAX_H
        # K must be between 1 and H//2
        K = random.randint(1, H // 2)
        test_case_lines = generate_test_case(X, Y, H, K)
        output_lines.extend(test_case_lines)

    return "\n".join(output_lines)

# Write to file or print
if __name__ == "__main__":
    input_data = generate_input()
    with open("max_input.in", "w") as f:
        f.write(input_data)
