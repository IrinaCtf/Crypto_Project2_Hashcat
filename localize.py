import hashlib
import math
from tag import *  # imports tag()

def localize(message: str, hashes1: list[str], hashes2: list[str]) -> int:
    """
    Detects the approximate location where corruption starts in the input message,
    by comparing recomputed SHA-256 hashes against two hash lists obtained from tag.py:
      - hashes1: computed from left-to-right (start-based)
      - hashes2: computed from right-to-left (end-based)

    Returns:
        An integer representing the *maximum* of the two estimated corruption start positions.
        Returns -1 if no corruption is detected.
    """

    def check_from_start(sub_msg: str, expected_hashes: list[str], offset: int = 0) -> int:
        """
        Recursively recomputes hashes from the start of the message using the same segmentation logic
        as tag.py's `helper_from_start`, and compares them against expected_hashes.

        Parameters:
            sub_msg (str): current substring to process
            expected_hashes (list): expected hashes for segments
            offset (int): running offset for current start position in the full message

        Returns:
            int: estimated index of corruption from start-based hashes, or -1 if all match
        """
        L = len(sub_msg)
        if L <= 0 or not expected_hashes:
            return -1

        if L <= 2:
            actual = hashlib.sha256(sub_msg.encode()).hexdigest()
            return offset if actual != expected_hashes[0] else -1

        # Find the largest k such that 2^(k+1) <= L
        k = int(math.floor(math.log2(L))) - 1
        if k < 0:
            actual = hashlib.sha256(sub_msg.encode()).hexdigest()
            return offset if actual != expected_hashes[0] else -1

        # Segment and hash [0:2^k] and [2^k:2^(k+1)]
        first = sub_msg[0:2**k]
        second = sub_msg[2**k:2**(k+1)]
        remaining = sub_msg[2**(k+1):]

        h1 = hashlib.sha256(first.encode()).hexdigest()
        h2 = hashlib.sha256(second.encode()).hexdigest()

        # Compare hashes and return offset if mismatch
        if h1 != expected_hashes[0]:
            return offset
        if h2 != expected_hashes[1]:
            return offset + 2**k

        # Recurse on remaining substring
        return check_from_start(remaining, expected_hashes[2:], offset + 2**(k+1))


    def check_from_end(sub_msg: str, expected_hashes: list[str], offset: int = 0) -> int:
        """
        Recursively checks segments from the end of the message. Returns the end index
        (relative to the original message) of the *first segment from the end* that matches
        its expected hash. If nothing matches, returns -1.

        Parameters:
            sub_msg (str): The current portion of the message to check
            expected_hashes (list): Hashes generated from end-to-start
            offset (int): Offset of sub_msg in original message (defaults to 0)

        Returns:
            int: The index marking the end of the first matching segment from the end,
                or -1 if no segment matches
        """
        L = len(sub_msg)
        if L <= 0 or not expected_hashes:
            return -1

        if L <= 2:
            actual = hashlib.sha256(sub_msg.encode()).hexdigest()
            return offset + L if actual == expected_hashes[-1] else -1

        k = int(math.floor(math.log2(L))) - 1
        if k < 0:
            actual = hashlib.sha256(sub_msg.encode()).hexdigest()
            return offset + L if actual == expected_hashes[-1] else -1

        seg1 = sub_msg[L - 2**k:]
        seg2 = sub_msg[L - 2**(k+1): L - 2**k]
        remaining = sub_msg[:L - 2**(k+1)]

        h1 = hashlib.sha256(seg1.encode()).hexdigest()
        h2 = hashlib.sha256(seg2.encode()).hexdigest()

        # If the latest (rightmost) segment matches, return its *end index*
        if h1 == expected_hashes[-1]:
            return offset + L
        elif h2 == expected_hashes[-2]:
            return offset + L - 2**k
        else:
            # Check earlier segments recursively
            return check_from_end(remaining, expected_hashes[:-2], offset)

    # Perform both checks
    start_index_1 = check_from_start(message, hashes1)
    if start_index_1 == -1: 
        start_index_1 = len(message)
    start_index_2 = check_from_end(message, hashes2)
    if start_index_2 == -1: 
        start_index_2 = 0

    # Return the max index as the most likely start of corruption
    # print(f"For debug: start_index_1 = {start_index_1}, start_index_2 = {start_index_2}")
    return max(start_index_1, start_index_2)


# Test code
if __name__ == "__main__":
    test_cases = [
        # (original, corrupted, expected index where insertion starts)
        ("a" * 64, "a" * 32 + "X" * 5 + "a" * 32, 32),                     # insert in middle
        ("abcdef" * 20, "abcdef" * 10 + "INSERTEDTEXT" + "abcdef" * 10, 60),  # balanced insert
        ("The quick brown fox jumps over the lazy dog",
         "The quick brown fox jumps INSERTED over the lazy dog", 25),
        ("abcdefghijklmnopqrstuvwxyz" * 3,
         "abcdefghijXklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz" * 2, 10),  # insert inside first rep
        ("1234567890" * 10,
         "1234567890" * 5 + "CORRUPTION" + "1234567890" * 5, 50),        # insert in exact half
        ("openai" * 100,
         "openai" * 70 + "EXTRAEXTRAEXTRA" + "openai" * 30, 420),        # large repeated pattern
        ("Data structures and algorithms are fun!" * 5,
         ("Data structures and algorithms are fun!" * 2) +
         ">>>GLITCH<<<" +
         ("Data structures and algorithms are fun!" * 3), 84),
        ("z" * 200,
         "z" * 199 + "Q", 199),  # very late corruption
    ]

    for i, (original, corrupted, expected) in enumerate(test_cases):
        ref_tags1, ref_tags2 = tag(original)
        result = localize(corrupted[:len(original)], ref_tags1, ref_tags2)
        if result == -1:
            result = len(original)
        print(f"Test case {i+1}: corruption starts at index {result} (expected: {expected}). L = {len(original)}. L' = {len(corrupted)}")
