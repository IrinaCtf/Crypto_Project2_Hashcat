import hashlib
import math
from tag import *  # imports tag()

def localize(corrupted_msg: str, reference_tags: list[str]) -> int:
    """
    Detect the starting index of an inserted segment in `corrupted_msg` by
    comparing on-the-fly SHA-256 hashes of segments with a reference hash list.

    Parameters:
    - corrupted_msg M': cut to the same length as M, because 0 <= i <= L.
    - reference_tags: list of hashes generated from the uncorrupted message via tag().

    Returns:
    - The predicted starting index i' in `corrupted_msg` where the inserted segment begins.
      If no mismatch is found, returns -1, which indicates that i = L.
    """
    
    def helper(msg: str, start_index: int, ref_tags: list[str], tag_idx: int) -> int:
        """
        Recursive helper to compare segments of `msg` with `ref_tags` hashes.
        
        Parameters:
        - msg: the current slice of the corrupted message to analyze.
        - start_index: the offset of this slice in the original `corrupted_msg`.
        - ref_tags: the list of original message hashes to compare against.
        - tag_idx: index into ref_tags for expected hash comparison.

        Returns:
        - The index in `corrupted_msg` where the corruption starts,
          or -1 if no corruption is found in this subtree.
        """
        L = len(msg)

        # Stop recursion if there's nothing to compare or tags are all used
        if L <= 0 or tag_idx >= len(ref_tags):
            return -1

        # Base case: short segment (length 2 or less), hash directly
        if L <= 2:
            current_hash = hashlib.sha256(msg.encode()).hexdigest()
            if current_hash != ref_tags[tag_idx]:
                return start_index  # mismatch found
            return -1  # match

        # Find the largest k such that 2^(k+1) <= L
        k = int(math.floor(math.log2(L))) - 1
        if k < 0:
            # Defensive fallback: treat whole msg as one segment
            current_hash = hashlib.sha256(msg.encode()).hexdigest()
            if current_hash != ref_tags[tag_idx]:
                return start_index
            return -1

        # Define segments according to the tagging logic
        seg1 = msg[0:2**k]                    # first part: [0 : 2^k]
        seg2 = msg[2**k:2**(k + 1)]           # second part: [2^k : 2^(k+1)]
        rest = msg[2**(k + 1):]               # remainder of message

        # Compare hash of seg1
        hash1 = hashlib.sha256(seg1.encode()).hexdigest()
        if hash1 != ref_tags[tag_idx]:
            return start_index  # mismatch in first segment

        # Compare hash of seg2
        hash2 = hashlib.sha256(seg2.encode()).hexdigest()
        if tag_idx + 1 < len(ref_tags) and hash2 != ref_tags[tag_idx + 1]:
            return start_index + 2**k  # mismatch in second segment

        # Recurse on the remaining part of the message
        return helper(rest, start_index + 2**(k + 1), ref_tags, tag_idx + 2)

    return helper(corrupted_msg, 0, reference_tags, 0)


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
        ref_tags = tag(original)
        result = localize(corrupted[:len(original)], ref_tags)
        if result == -1:
            result = len(original)
        print(f"Test case {i+1}: corruption starts at index {result} (expected: {expected}). L = {len(original)}. L' = {len(corrupted)}")
