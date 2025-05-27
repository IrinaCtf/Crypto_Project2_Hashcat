import os
from tag import tag
from localize import localize

# Toggle between inline tests and reading from testcase/*.txt files
READ_FROM_TXT = False

def find_expected_range(original: str, corrupted: str) -> tuple[int, int]:
    """
    Compares original and corrupted strings character-by-character.
    Returns a tuple: (start_index i, end_index j) of the corrupted range relative to the corrupted message.
    """
    start = 0
    while start < len(original) and start < len(corrupted) and original[start] == corrupted[start]:
        start += 1

    end = 0
    while end < len(original) and end < len(corrupted) and original[-1 - end] == corrupted[-1 - end]:
        end += 1

    return start, len(corrupted) - end - 1

def calculate_localize_factor(i: int, j: int, i_prime: int, j_prime: int) -> float:
    """
    Calculates localization accuracy factor: |i - j + 1| / |i' - j' + 1|
    where (i, j) are the true start and end indices, and (i', j') are the predicted indices.
    Returns:
        float: the localization factor (higher is worse; 1 is perfect)
    """
    true_range = j - i + 1
    predicted_range = j_prime - i_prime + 1
    if predicted_range == 0:
        return float('inf') # Avoid division by zero
    return abs(true_range / predicted_range)

def evaluate_case(original: str, corrupted: str, case_name: str):
    """
    Run a single corruption detection test using tag and localize on both forward and reverse strings.
    Print predicted and expected start/end of corruption, localization factor, and hash count.
    """
    i_expected, j_expected = find_expected_range(original, corrupted)

    # Predict i': start of corruption
    tags1_start, tags2_start = tag(original)
    i_prime = localize(corrupted[:len(original)], tags1_start, tags2_start)

    # Predict j': end of corruption using reversed strings
    original_rev = original[::-1]
    corrupted_rev = corrupted[::-1]
    tags1_end, tags2_end = tag(original_rev)
    j_prime_rev = localize(corrupted_rev[:len(original)], tags1_end, tags2_end)
    # print(j_prime_rev)
    j_prime = len(corrupted) - j_prime_rev - 1 if j_prime_rev != -1 else -1
    # print(original_rev, corrupted_rev, j_prime_rev, sep = "\n")

    # Calculate factor
    factor = calculate_localize_factor(i_expected, j_expected, i_prime, j_prime)

    # Total number of hash tags used (both forward and reverse)
    num_hashes_used = len(tags1_start) + len(tags2_start)

    print(f"[{case_name}]")
    print(f"  Message Length = {len(original)}; Corruption Length: {j_expected - i_expected + 1}")
    print(f"  Localization Factor: {factor:.2f}; Hashes Used: {num_hashes_used}")

def run_inline_tests():
    test_cases = [
        # One insertion in the middle
        ("abcdefghijabcdefghij", "abcdefghijHELLOabcdefghij"),
        # One short insertion in middle
        ("hellotheregeneral", "hello123theregeneral"),
        # One long insertion in middle
        ("datastructuresandalgos", "datastructuresINSERTIONandalgos"),
        # Insertion of special characters
        ("opensesameopen", "opensesa@@@meopen"),
        # Numeric insertion
        ("zipzapzoom", "zip777zapzoom"),
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
