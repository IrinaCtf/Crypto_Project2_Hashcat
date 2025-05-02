import math

class Detective:
        
    def __init__(self, limit:int):
        """
        limit: determines the number upto which primes are generated
        """
        assert(limit > 0)

        self.__lvl = self._gen_primes(limit)
        # print(self.__primes)
        print(self.__lvl)

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

    def detect(self):
        pass