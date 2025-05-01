import random

def generate_nested_term(depth, var_base='X'):
    """Create a deeply nested term like f(f(f(...X)))"""
    term = var_base
    for _ in range(depth):
        functor = random.choice('fghklmn')
        term = f'({functor} {term})'
    return term

def generate_chained_substitution(depth):
    """
    Create a chain of substitutions like:
    (f A), (f (g B)), (f (g (h C)))...
    """
    term1 = f'(f A)'
    term2 = '(f ' + generate_nested_term(depth, 'B') + ')'
    return term1, term2

def generate_occurs_check_case(depth):
    """Create a term like X and (f (f ... (X))) to force occurs check."""
    return 'X', generate_nested_term(depth, 'X')

def generate_arity_bomb():
    """Terms that have many flat arguments to blow up term comparisons."""
    n = 100
    args1 = ' '.join(['a'] * n)
    args2 = ' '.join(['a'] * (n - 1) + ['b'])  # One mismatch
    return f'(p {args1})', f'(p {args2})'

def generate_max_len():
    return '(' + 'A ' * 98 + 'A' + ')', '(' + 'B ' * 98 + 'B' + ')'

def generate_max_nested():
    return '(' * 99 + 'A' + ')' * 99, '(' * 99 + 'B' + ')' * 99

def write_test_cases(n=50, filename='worst_unification_cases.in'):
    with open(filename, 'w') as f:
        f.write(str(n) + '\n')
        for i in range(n):
            if i % 5 == 0:
                t1, t2 = generate_occurs_check_case(depth=100)
            elif i % 5 == 1:
                t1, t2 = generate_chained_substitution(depth=100)
            elif i % 5 == 2:
                t1, t2 = generate_arity_bomb()
            elif i % 5 == 3:
                t1, t2 = generate_max_len()
            elif i % 5 == 4:
                t1, t2 = generate_max_nested()
            f.write(f"{t1} {t2}\n")

# Generate the file
write_test_cases(n=1000)
print("Generated 'worst_unification_cases.txt' with 100 stress test cases.")
