# main.py
import hashlib as hl
from detect import Detective, randCorruptSeq
from localize import bin_localize

def segement_analysis(original_superset, corrupted_superset, level, i,j):
    diff = 0
    for m in range(0, len(original_superset[level])):
        if(original_superset[level][m] != corrupted_superset[level][m]):
            diff += 1
    pref_res = diff/len(original_superset[level])
    act_res = abs(j-i)/len(original_superset[level])
    final_res = abs(pref_res-act_res)*100
    print("Analysis by segment on level "+str(level)+" With Actual differences as " +str(round(pref_res,2)) + " Our findings on the difference as "+ str(round(act_res,2)) + "\nLocalization Factor of "+str(round(100-final_res,2))+"%" )  


def main():
    # Step 1: Open test file and read content
    with open("test.txt", "r") as file:
        lines = file.readlines()
        if len(lines) < 2:
            print("Test file must have at least two lines: original and corrupted message.")
            return
        original_message = lines[0].strip()
        corrupted_message = lines[1].strip()[:len(original_message)]

    # Step 2: Create Detective instance
    limit = 2 * len(original_message)
    hash_func = lambda x: hl.md5(x.encode('ascii')).hexdigest()
    agent = Detective(limit, hash_func)

    # Step 3: Get superset hashes
    
    original_superset = agent.superSet(original_message)

    # Step 4: Get list of primes
    prime_list = agent.primes()

    # Step 5: Print results
    
    #corrupted, target = randCorruptSeq(original_message, 5)
    #agent.remember(original_message)
    #print("MAIN "+str(agent.inspect(corrupted)))
    #print(f'Error at {target}')
    # Step 6: Perform binary search and localize
    i, j, corrupted_text, corrupted_superset,level = bin_localize(agent, corrupted_message, original_superset)
    print("Start of corruption index i':"+str(i) +"\tEnd of corruption index j':"+str(j) +"\nCorrupted Hashes " + str(corrupted_text))

    # Step 7: Analysis TO DO
    segement_analysis(original_superset, corrupted_superset, i,j,level)

if __name__ == "__main__":
    main()
