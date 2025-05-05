import hashlib
import math

def tag(message: str) -> list[str]:
    """
    Generate a list of SHA-256 hash digests from the message.
    The message is recursively split into two parts:
      [0 : 2^k] and [2^k : 2^(k+1)], where k is the largest integer
      such that 2^(k+1) <= len(message).
    The same process is applied recursively to the remaining message
    from index 2^(k+1) onward, until the length is <= 2.
    Each valid segment is hashed and added to the result list.
    """
    def helper(sub_msg: str) -> list[str]:
        L = len(sub_msg)
        if L <= 0: return []
        # Base case: if the message is length 2 or less, hash it directly
        if L <= 2:
            return [hashlib.sha256(sub_msg.encode()).hexdigest()] if L > 0 else []

        # Compute the largest k such that 2^(k+1) <= L
        k = int(math.floor(math.log2(L))) - 1
        if k < 0:
            return [hashlib.sha256(sub_msg.encode()).hexdigest()]

        # Define the segments: [0:2^k] and [2^k:2^(k+1)]
        first = sub_msg[0:2**k]
        second = sub_msg[2**k:2**(k+1)]
        remaining = sub_msg[2**(k+1):]

        # Compute SHA-256 hashes of the two segments
        hashes = [
            hashlib.sha256(first.encode()).hexdigest(),
            hashlib.sha256(second.encode()).hexdigest()
        ]

        # Recurse on the remaining message and return full list
        return hashes + helper(remaining)

    return helper(message)

# Test code
if __name__ == "__main__":
    test_messages = [
        "",                           # empty
        "a",                          # 1 char
        "hi",                         # 2 chars
        "hello!",                     # short msg
        "abcdefghijklmno",            # 15 chars
        "abcdefghijklmnopqrstuvwxyz", # 26 chars
        "The quick brown fox jumps over the lazy dog"
    ]

    for i, msg in enumerate(test_messages):
        print(f"\nTest case {i+1}: \"{msg}\"")
        hashtags = tag(msg)
        print(f"Generated {len(hashtags)} hash(es):")
        for j, h in enumerate(hashtags):
            print(f"  [{j}] {h}")
