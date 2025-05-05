import os

def write_testcase(original: str, corrupted: str, folder: str = "testcase"):
    """
    Writes a new test case file into the testcase/ folder.
    The file is named as testcase#.txt, where # is the smallest unused index.
    Each file contains two lines: the original string and the corrupted string.
    """
    # Ensure the folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Find the smallest unused integer for the filename
    i = 0
    while os.path.exists(os.path.join(folder, f"testcase{i}.txt")):
        i += 1

    filename = os.path.join(folder, f"testcase{i}.txt")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(original.strip() + "\n")
        f.write(corrupted.strip() + "\n")

    print(f"Success: Test case written to {filename}")

# Example usage
if __name__ == "__main__":
    original = "a" * 64
    corrupted = "a" * 32 + "X" * 5 + "a" * 32
    write_testcase(original, corrupted)
