import hashlib
import math
from typing import Union
from tag import *  # original tag() that returns list[str]

def localize(message: str, hashes1: list[str], hashes2: list[str]) -> Union[tuple[int, int], int]:
    """
    Detects a corruption window by comparing hash segments.
    Returns (i, j) as the estimated corruption range: [i, j)
    """

    def check_from_start(sub_msg: str, expected_hashes: list[str], offset: int = 0) -> Union[tuple[int, int], None]:
        L = len(sub_msg)
        if L <= 0 or not expected_hashes:
            return None

        if L <= 2:
            h = hashlib.sha256(sub_msg.encode()).hexdigest()
            if h != expected_hashes[0]:
                return (offset, offset + L)
            else:
                return None

        k = int(math.floor(math.log2(L))) - 1
        if k < 0:
            h = hashlib.sha256(sub_msg.encode()).hexdigest()
            if h != expected_hashes[0]:
                return (offset, offset + L)
            else:
                return None

        p = 2**k
        q = 2**(k + 1)

        h1 = hashlib.sha256(sub_msg[0:p].encode()).hexdigest()
        h2 = hashlib.sha256(sub_msg[p:q].encode()).hexdigest()

        if h1 != expected_hashes[0]:
            return (offset, offset + p)
        if h2 != expected_hashes[1]:
            return (offset + p, offset + q)

        return check_from_start(sub_msg[q:], expected_hashes[2:], offset + q)

    def check_from_end(sub_msg: str, expected_hashes: list[str], offset: int = 0) -> Union[tuple[int, int], None]:
        L = len(sub_msg)
        if L <= 0 or not expected_hashes:
            return None

        if L <= 2:
            h = hashlib.sha256(sub_msg.encode()).hexdigest()
            if h == expected_hashes[-1]:
                return None
            else:
                return (offset, offset + L)

        k = int(math.floor(math.log2(L))) - 1
        if k < 0:
            h = hashlib.sha256(sub_msg.encode()).hexdigest()
            if h == expected_hashes[-1]:
                return None
            else:
                return (offset, offset + L)

        p = 2**k
        q = 2**(k + 1)

        seg1 = sub_msg[L - p:]
        seg2 = sub_msg[L - q:L - p]

        h1 = hashlib.sha256(seg1.encode()).hexdigest()
        h2 = hashlib.sha256(seg2.encode()).hexdigest()

        if h1 == expected_hashes[-1]:
            return None
        if h2 == expected_hashes[-2]:
            return (offset + L - p, offset + L)

        result = check_from_end(sub_msg[:L - q], expected_hashes[:-2], offset)
        if result is None:
            return (offset + L - q, offset + L)
        else:
            return result

    start_result = check_from_start(message, hashes1)
    end_result = check_from_end(message, hashes2)
    print("start_result and end_results are: ", start_result, end_result, end = ";")
    if not start_result and not end_result:
        return -1

    i = max(start_result[0] if start_result else 0,
            end_result[0] if end_result else 0)
    j = min(start_result[1] if start_result else len(message),
            end_result[1] if end_result else len(message))

    return (i, j)


# Optional test
if __name__ == "__main__":
    original = "a" * 32 + "b" * 32
    corrupted = "a" * 30 + "XX" + "b" * 32
    h1, h2 = tag(original)
    print("Corruption range:", localize(corrupted[:len(original)], h1, h2))
