# main.py
import hashlib as hl
from detect import Detective
from localize import localize, binary_search 

def main():
    # Step 1: Open test file and read content
    with open("test.txt", "r") as file:
        lines = file.readlines()
        if len(lines) < 2:
            print("Test file must have at least two lines: original and corrupted message.")
            return
        original_message = lines[0].strip()
        corrupted_message = lines[1].strip()[:len(original_message)]
    '''
    Are we handling the length difference the way above? Just abandon the longer part???
    '''

    # Step 2: Create Detective instance
    limit = 2 * len(original_message)
    hash_func = lambda x:x  #lambda x: hl.md5(x.encode('ascii')).hexdigest()
    agent = Detective(limit, hash_func)

    # Step 3: Get superset hashes

    original_superset = agent.superSet(original_message)

    #TO DO: to localize function in localize.py once done
    corrupted_superset = agent.superSet(corrupted_message)

    # Step 4: Get list of primes
    prime_list = agent.primes()

    # Step 5: Print results
    print("Original Superset Hashes:")
    for segment in original_superset:
        print(segment)

    print("\nCorrupted Superset Hashes:")
    for segment in corrupted_superset:
        print(segment)

    print("\nList of Primes:")
    print(prime_list)
    print("CASE 1")
    ogHash, cHash, start_index, lvl = binary_search(original_superset,corrupted_superset, 0,0)
    print("MAIN " + ogHash[lvl][start_index] + " "+ cHash[lvl][start_index])

if __name__ == "__main__":
    main()
