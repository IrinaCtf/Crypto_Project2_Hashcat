import math
from detect import Detective


# driver function that first conducts binary search
# results from binary search are taken to localize to find adjacent corruptions
def bin_localize(agent, corrupted_message, original_hashset):
    corrupted_hashset = agent.superSet(corrupted_message)
    ogHash, cHash, start_index, lvl = binary_search(original_hashset,corrupted_hashset, 0,0)
    return localize(ogHash, cHash, start_index, lvl)


def binary_search(ogHash, cHash, mid, level):
    
    #search for corruption in depth
    if level >= math.sqrt(len(ogHash)):
        return (ogHash, cHash, mid, level-1)
    else: # Check base case
        high = len(ogHash[level])
        low = 0
        if high > low:

            mid = (high + low) // 2

            # If element is present at the middle itself
            if ogHash[level][mid] != cHash[level][mid]:
                return binary_search(ogHash, cHash, mid, level + 1)

            # If element is equal at mid, then it can only
            # be present in left subarray or the latter half
            elif ogHash[level][mid] == cHash[level][mid]:
                return binary_search(ogHash, cHash, mid+1, level +1)

        else:

            return (ogHash,cHash,0, 0)


def localize(ogHash, cHash, start_index, level):

    corrupt_len = len(cHash[level])
    checked = 1
    counter = 0
    k = start_index
    begin_corrupt_index = corrupt_len
    end_corrupt_index = -1
    '''
    case 0: only one index was corrupted so checked needs to start at 0
    this can mean that we can stop searching too hence the break

    case 1: there are no more continuous corruptions on one end 
    so we don't need to keep checking that end

    case 2: we've checked all we can of one end so we set their index 
    so we don't need to keep checking that end
    '''
    while(counter < corrupt_len):

        #check that we found the whole corruption
        if(begin_corrupt_index != corrupt_len and end_corrupt_index != -1):
            break
        #check that we haven't reached the end
        if(k + checked >= corrupt_len):
            end_corrupt_index = corrupt_len 

        #check that we haven't reached past the start
        if(k - checked < 0):
            begin_corrupt_index = 0
        
        #check end
        if(end_corrupt_index == -1 and cHash[level][k+checked] == ogHash[level][k+checked]):
            end_corrupt_index = k + checked


        #check beginning
        if(begin_corrupt_index == corrupt_len and cHash[level][k-checked] == ogHash[level][k-checked]):
            begin_corrupt_index = k - checked + 1

        #increment counters
        checked +=1
        counter +=1

    return (begin_corrupt_index, end_corrupt_index, cHash[level][begin_corrupt_index:end_corrupt_index], cHash, level)  
