# Number of test cases
num_test_cases = 1
print(num_test_cases)

# Define parameters: levels of nesting and repeat count
levels = 30
C = 2

# Calculate total number of lines
K = 2 * levels + 1
print(K)

# Generate the GO program lines
for line in range(1, K + 1):
    if line <= levels:
        # First 'levels' lines are skips
        print("skip")
    elif line <= 2 * levels:
        # Next 'levels' lines are repeat commands
        M = 2 * levels - line + 1
        print(f"repeat {M} {C}")
    else:
        # Last line is stop
        print("stop")
