import os
from tag import tag
from localize import localize

# Toggle between inline tests and reading from testcase/*.txt files
READ_FROM_TXT = False

def find_expected_range(original: str, corrupted: str) -> tuple[int, int]:
    start = 0
    while start < len(original) and start < len(corrupted) and original[start] == corrupted[start]:
        start += 1

    end = 0
    while end < len(original) and end < len(corrupted) and original[-1 - end] == corrupted[-1 - end]:
        end += 1

    return start, len(corrupted) - end - 1

def calculate_localize_factor(i: int, j: int, i_prime: int, j_prime: int) -> float:
    true_range = j - i + 1
    predicted_range = j_prime - i_prime + 1
    if predicted_range == 0:
        return float('inf')
    return true_range / predicted_range

def localize_once(original: str, corrupted: str) -> tuple[int, int]:
    tags1_start, tags2_start = tag(original)
    i_prime = localize(corrupted[:len(original)], tags1_start, tags2_start)

    original_rev = original[::-1]
    corrupted_rev = corrupted[::-1]
    tags1_end, tags2_end = tag(original_rev)
    j_prime_rev = localize(corrupted_rev[:len(original)], tags1_end, tags2_end)
    j_prime = len(corrupted) - j_prime_rev - 1 if j_prime_rev != -1 else -1

    return i_prime, j_prime

def evaluate_case(original: str, corrupted: str, case_name: str):
    i_expected, j_expected = find_expected_range(original, corrupted)

    L = len(original)
    c = 16 #self-defined
    rotations = L // c

    best_i_prime = -1
    best_j_prime = len(corrupted)

    for r in range(rotations):
        offset = r * c

        rotated_original = original[offset:] + original[:offset]
        rotated_corrupted = corrupted[offset:] + corrupted[:offset]

        i_r, j_r = localize_once(rotated_original, rotated_corrupted)

        if i_r != -1:
            i_unrotated = (i_r - offset + len(corrupted)) % len(corrupted)
            best_i_prime = max(best_i_prime, i_unrotated)
        if j_r != -1:
            j_unrotated = (j_r - offset + len(corrupted)) % len(corrupted)
            best_j_prime = min(best_j_prime, j_unrotated)

    factor = calculate_localize_factor(i_expected, j_expected, best_i_prime, best_j_prime)
    num_hashes_used = len(tag(original)[0]) + len(tag(original)[1])

    print(f"[{case_name}]")
    print(f"  Expected: i = {i_expected}, j = {j_expected}")
    print(f"  Predicted: i' = {best_i_prime}, j' = {best_j_prime}")
    print(f"  Localization Factor: {factor:.2f}; Hashes Used: {num_hashes_used}")

def run_inline_tests():
    test_cases = [
        ("a" * 64, "a" * 32 + "X" * 5 + "a" * 32),
        ("abcdef" * 20, "abcdef" * 10 + "INSERTEDTEXT" + "abcdef" * 10),
        ("The quick brown fox jumps over the lazy dog",
         "The quick brown fox jumps INSERTED over the lazy dog"),
        ("abcdefghijklmnopqrstuvwxyz" * 3,
         "abcdefghijXklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz" * 2),
        ("1234567890" * 10,
         "1234567890" * 5 + "CORRUPTION" + "1234567890" * 5),
        ("openai" * 100,
         "openai" * 70 + "EXTRAEXTRAEXTRA" + "openai" * 30),
        ("Data structures and algorithms are fun!" * 5,
         ("Data structures and algorithms are fun!" * 2) +
         ">>>GLITCH<<<" +
         ("Data structures and algorithms are fun!" * 3)),
        ("z" * 200, "z" * 199 + "Q"),
    ]

    for i, (original, corrupted) in enumerate(test_cases):
        evaluate_case(original, corrupted, f"Inline Test {i+1}")

def run_txt_tests(folder_path="testcase"):
    if not os.path.exists(folder_path):
        print(f"Error: folder '{folder_path}' does not exist.")
        return

    for filename in sorted(os.listdir(folder_path)):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(folder_path, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()

            if len(lines) < 2:
                print(f"[{filename}] Error: File must contain at least 2 lines (original and corrupted).")
                continue

            original = lines[0].strip()
            corrupted = lines[1].strip()

            if len(original) >= len(corrupted):
                print(f"[{filename}] Error: L >= L'. Only single insertion corruption allowed.")
                continue

            evaluate_case(original, corrupted, filename)

        except Exception as e:
            print(f"[{filename}] Error reading file: {e}")

if __name__ == "__main__":
    print(f"READ_FROM_TXT set to {READ_FROM_TXT}. ", end="")
    if READ_FROM_TXT:
        print("To run inline tests, set READ_FROM_TXT to False.")
        run_txt_tests()
    else:
        print("To run tests from txt files, set READ_FROM_TXT to True.")
        run_inline_tests()
