from detect import *
from localize import *

'''
We send the hash of OG msg and received msg and compare the hashes
any hash that is not EXACTLY the same is corrupt and gets sent to localization
'''
def corruptHashDetect():
    return 0

'''
This is to narrow down the exact start and end index of the corruption
We use binary search to first find the corruption in general
options to narrow it down further
- binary search again but we factor in the expected length of the corruption
so you could instead of checking in halves based on the lenght of the hash
we now check based on halves of the corruption length
- check each adjacent bit/index and compare w og hash and keep going until we get to the start or end
- ???
'''
def localization():
    return 0

