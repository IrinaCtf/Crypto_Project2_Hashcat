import hashlib as hl

class Detective:
        
    def __init__(self, limit:int, hashFunc):
        """
        limit: determines the number upto which primes are generated
        hashFunc: a hard predicate that takes encoded strings as input and throws a hex hash digest out
        """
        try:
            assert(limit > 0)
        except:
            print(f"ERR: limit {limit} is non-positive!")
            exit(1)
        
        try:
            assert(hashFunc("hashable") != None)
        except:
            print(f"ERR: hash function compuation failure!")
            exit(1)

        self.__lvl = self._gen_primes(limit)
        self.__hash = hashFunc

        # print(self.__primes)
        # print('Lvl:', self.__lvl)

        pass

    def _gen_primes(self, limit:int) -> int:
        """
        upto the limit, collects all primes. Returns number of primes, pi(x)
        Uses Sieve of Eratosthenes
        """
        if limit < 2:
            self.__primes = []
            return 0
        
        primes = [ 2 ]

        for number in range(3, limit + 1):
            isPrime = True
            for prime in primes:
                if number % prime == 0:
                    isPrime = False
            
            if isPrime:
                primes.append(number)
        
        self.__primes = primes

        return len(primes)

    def detect(self, message) -> tuple:
        # define segment hash supersets, self.__lvl in size
        self.__segmentset = []

        for segmentCount in range(0, self.__lvl):
            segments = []
            width = len(message) // self.__primes[segmentCount]
            
            for idx in range(0, self.__primes[segmentCount]):
                segmentHash = self.__hash(message[idx : idx + width])
                segments.append(segmentHash)
            
            self.__segmentset.append(segments)
        
        return self.__segmentset



message = "this is a secret"
gadget = Detective(len(message), lambda x: hl.md5(x.encode('ascii')).hexdigest())

print(gadget.detect(message))