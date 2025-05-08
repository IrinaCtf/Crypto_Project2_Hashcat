# experiment.py

import random
import string
import statistics
from tag import tag
from localize import localize
from main import calculate_localize_factor

def generate_random_message(length: int) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def insert_corruption(original: str, corruption_len: int) -> tuple[str, int, int]:
    corruption = ''.join(random.choices(string.ascii_letters + string.digits, k=corruption_len))
    insert_index = random.randint(0, len(original))
    corrupted = original[:insert_index] + corruption + original[insert_index:]
    return corrupted, insert_index, insert_index + corruption_len - 1

def run_single_experiment(a: int, b: int) -> float:
    original = generate_random_message(a)
    corrupted, i_expected, j_expected = insert_corruption(original, b)

    # Predict i'
    tags1_start, tags2_start = tag(original)
    i_prime = localize(corrupted[:len(original)], tags1_start, tags2_start)

    # Predict j'
    original_rev = original[::-1]
    corrupted_rev = corrupted[::-1]
    tags1_end, tags2_end = tag(original_rev)
    j_prime_rev = localize(corrupted_rev[:len(original)], tags1_end, tags2_end)
    j_prime = len(corrupted) - j_prime_rev - 1 if j_prime_rev != -1 else -1

    factor = calculate_localize_factor(i_expected, j_expected, i_prime, j_prime)
    return factor

def run_experiments(num_runs: int, a: int, b: int):
    factors = []
    for i in range(num_runs):
        factor = run_single_experiment(a, b)
        factors.append(factor)

    print(f"\n=== Experiment Results over {num_runs} trials (a={a}, b={b}) ===")
    print(f"Min Localization Factor:     {min(factors):.4f}")
    print(f"Max Localization Factor:     {max(factors):.4f}")
    print(f"Average Localization Factor: {statistics.mean(factors):.4f}")
    print(f"Std Dev Localization Factor: {statistics.stdev(factors):.4f}")

if __name__ == "__main__":
    NUM_RUNS = 1000   # Number of randomized trials
    A = 1000        # Message length
    B = 50        # Corruption length

    run_experiments(NUM_RUNS, A, B)
