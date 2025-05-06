
#when calling send M hash, M' hash
def binary_search(ogHash, cHash, mid):
    high = len(ogHash)
    low = 0

    # Check base case
    if high > low:

        mid = (high + low) // 2

        # If element is present at the middle itself
        if ogHash[mid] != cHash[mid]:
            print(ogHash +" "+ cHash)
            return (ogHash, cHash, mid)

        # If element is equal at mid, then it can only
        # be present in left subarray or the latter half
        elif ogHash[mid] == cHash[mid]:
            print(ogHash +" "+ cHash)
            return binary_search(ogHash[mid+1:], cHash[mid+1:], mid+1)

    else:
        # Everything is equal
        print("equal")
        return (ogHash,cHash,0)


def localize(ogHash, cHash, start_index):

    corrupt_len = len(cHash)
    checked = 1
    counter = 0
    k = start_index
    begin_corrupt_index = -1
    end_corrupt_index = -1
    print("start w "+ str(k))
    '''
    case 0: only one index was corrupted so checked needs to start at 0
    this can mean that we can stop searching too hence the break

    case 1: there are no more continuous corruptions on one end 
    so we don't need to keep checking that end

    case 2: we've checked all we can of one end so we set their index 
    so we don't need to keep checking that end
    '''
    while(counter < corrupt_len):
        print(counter)
        #check that we haven't reached the end
        if(k + checked >= corrupt_len):
            end_corrupt_index = corrupt_len
        #check that we haven't reached the start
        if(k - checked < 0):
            begin_corrupt_index = 0
        
        #check that we found the whole corruption
        if(begin_corrupt_index != -1 and end_corrupt_index != -1):
            break

        #check end
        if(end_corrupt_index == -1 and cHash[k+checked] == ogHash[k+checked]):
            end_corrupt_index = k + checked - 1
            #checked += 1
            print("end counter "+ str(counter))

        #check beginning
        if(begin_corrupt_index == -1 and cHash[k-checked] == ogHash[k-checked]):
            begin_corrupt_index = k - checked + 1
            #checked += 1
            print("begin counter "+ str(counter))
        checked +=1
        counter +=1
    return (begin_corrupt_index, end_corrupt_index, cHash[begin_corrupt_index:end_corrupt_index])  




print("CASE 1")
ogHash, cHash, start_index = binary_search("HelloHelloHello","HelloHelloHe110", 0)
print(localize(ogHash, cHash, start_index))

print("CASE 2")
ogHash, cHash, start_index = binary_search("HelloHelloHello","HelloHelloHe1lo", 0)
print(localize(ogHash, cHash, start_index))

print("CASE 3")
ogHash, cHash, start_index = binary_search("HelloHelloHello","HelloBYeyeHe1lo", 0)
print(localize(ogHash, cHash, start_index))

print("CASE 4")
ogHash, cHash, start_index = binary_search("HelloHelloHello","BybebHelloHello", 0)
print(localize(ogHash, cHash, start_index))