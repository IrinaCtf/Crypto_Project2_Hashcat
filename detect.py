import math

class Detective:
        
    def __init__(self, limit:int):
        """
        limit: determines the number upto which primes are generated
        """
        assert(limit > 0)

        self.__lvl = self._gen_primes(limit)
        pass
    
    def gen_primes(self, limit:int):
        pass