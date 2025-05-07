# main.py
import hashlib as hl
from detect import Detective
from localize import bin_localize


def main():
    # Step 1: Open test file and read content
    with open("test.txt", "r") as file:
        lines = file.readlines()
        if len(lines) < 2:
            print("Test file must have at least two lines: original and corrupted message.")
            return
        original_message = lines[0].strip()
        corrupted_message = lines[1].strip()[:len(original_message)]

    #TO DO: DELETE ONCE ALL TESTING IS DONE
    #original_message = "HelloHelloHello"
    #corrupted_message = "HelloGoodbHello"

    # Step 2: Create Detective instance
    limit = 2 * len(original_message)
    hash_func = lambda x: hl.md5(x.encode('ascii')).hexdigest()
    agent = Detective(limit, hash_func)

    # Step 3: Get superset hashes
    
    original_superset = agent.superSet(original_message)

    # Step 4: Get list of primes
    prime_list = agent.primes()

    # Step 5: Print results
    print("Original Superset Hashes:")
    for segment in original_superset:
        print(segment)

    # Step 6: Perform binary search and localize
    i, j, corrupted_text = bin_localize(agent, corrupted_message, original_superset)
    print("Start of corruption index i':"+str(i) +"\tEnd of corruption index j':"+str(j) +"\nCorrupted Hashes " + str(corrupted_text))

    # Step 7: Analysis TO DO


if __name__ == "__main__":
    main()
