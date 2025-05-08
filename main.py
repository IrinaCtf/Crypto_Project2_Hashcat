# main.py
import hashlib as hl
from detect import Detective, randCorruptSeq
from localize import bin_localize
import statistics

def segement_analysis(original_superset, corrupted_superset, level, i,j):
    diff = 0
    for m in range(0, len(original_superset[level])):
        if(original_superset[level][m] != corrupted_superset[level][m]):
            diff += 1
    pref_res = diff/len(original_superset[level])
    act_res = abs(j-i)/len(original_superset[level])
    final_res = abs(pref_res-act_res)*100
    print("Analysis by segment on level "+str(level)+"\nWith Actual differences as " +str(round(pref_res,2)) + " Our findings on the difference as "+ str(round(act_res,2)) + "\nLocalization Factor of "+str(round(100-final_res,2))+"%" )  





def single_index_analysis(og_len, ip,jp, level,prime_list, target):

    msg_len = og_len // prime_list[level]
    print("Analysis by index \nActual index "+str(target)+ " Our findings as (" +str(ip*msg_len) + ", "+str(jp*msg_len)+")")
    loc_beg = abs((ip*msg_len)-target[0])
    print("Beginning Index Localization factor off by "+str(loc_beg))
    loc_end = abs((jp*msg_len)-target[1])
    print("Ending Index Localization factor off by "+str(loc_end))
    return (loc_beg, loc_end)

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
    beg_index_list = []
    end_index_list = []
    # Step 5: Create a variety of corrupted messages
    for k in range(0,10):
        print("ROUND "+str(k))
        corrupted_message, target = randCorruptSeq(original_message, 5)
        agent.remember(original_message)
        # Step 6: Perform binary search and localize
        
        i, j, corrupted_text, corrupted_superset,level = bin_localize(agent, corrupted_message, original_superset)
        print("Start of corruption index i':"+str(i) +"\tEnd of corruption index j':"+str(j))

        # Step 7: Analysis TO DO
        segement_analysis(original_superset, corrupted_superset, i,j,level)
        idiff, jdiff = single_index_analysis(len(original_message), i,j,level, prime_list, target)
        beg_index_list.append(idiff)
        end_index_list.append(jdiff)

    print("Final average beginning localization factor is "+str(statistics.mean(beg_index_list)))
    print("Final average ending localization factor is "+str(statistics.mean(end_index_list)))

if __name__ == "__main__":
    main()
