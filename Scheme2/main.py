import os
from tag import tag
from localize import localize

# Toggle between inline tests and reading from testcase/*.txt files
READ_FROM_TXT = False

def run_inline_tests():
    test_cases = [
        # (original, corrupted, expected index)
        ("a" * 64, "a" * 32 + "X" * 5 + "a" * 32, 32),
        ("abcdef" * 20, "abcdef" * 10 + "INSERTEDTEXT" + "abcdef" * 10, 60),
        ("The quick brown fox jumps over the lazy dog",
         "The quick brown fox jumps INSERTED over the lazy dog", 25),
        ("abcdefghijklmnopqrstuvwxyz" * 3,
         "abcdefghijXklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz" * 2, 10),
        ("1234567890" * 10,
         "1234567890" * 5 + "CORRUPTION" + "1234567890" * 5, 50),
        ("openai" * 100,
         "openai" * 70 + "EXTRAEXTRAEXTRA" + "openai" * 30, 420),
        ("Data structures and algorithms are fun!" * 5,
         ("Data structures and algorithms are fun!" * 2) +
         ">>>GLITCH<<<" +
         ("Data structures and algorithms are fun!" * 3), 84),
        ("z" * 200,
         "z" * 199 + "Q", 199),
    ]

    for i, (original, corrupted, expected) in enumerate(test_cases):
        ref_tags = tag(original)
        result = localize(corrupted[:len(original)], ref_tags)
        print(f"[Inline Test {i+1}] Corruption at index {result} (expected {expected})")

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

            ref_tags = tag(original)
            result = localize(corrupted[:len(original)], ref_tags)
            if result == -1:
                result = len(original)
            print(f"[{filename}] Corruption starts at index {result}. L = {len(original)}. L' = {len(corrupted)}")

        except Exception as e:
            print(f"[{filename}] Error reading file: {e}")

if __name__ == "__main__":
    print(f"READ_FROM_TXT set to {READ_FROM_TXT}. ", end = "")
    if READ_FROM_TXT:
        print("To run inline tests, set READ_FROM_TXT to be True")
        run_txt_tests()
    else:
        print("To run tests from txt files, set READ_FROM_TXT to be False")
        run_inline_tests()
