from random import randint

class Error:
    @classmethod
    def singleError(cls, data):
        n = len(data)
        # n = 31
        index = randint(0, n - 1)
        edata = ""
        for i in range(len(data)):
            if i == index:
                edata += str((int(data[i])) ^ 1)
            else:
                edata += data[i]
        return edata
    @classmethod
    def completeBurstError(cls, data):
        n = len(data)
        # n = 31
        indexl = randint(0, n - 1)
        indexr = randint(indexl, n - 1)
        edata = ""
        for i in range(len(data)):
            if i >= indexl and i <= indexr:
                edata += str((int(data[i])) ^ 1)
            else:
                edata += data[i]
        return edata
    @classmethod
    def burstError(cls, data):
        n = len(data)
        # n = 31
        indices = [i for i in range(n)]
        # shuffle
        for i in range(n):
            swapind = randint(i, n - 1)
            indices[i], indices[swapind] = indices[swapind], indices[i]
        m = randint(1, n)
        s = set()
        for i in range(m):
            s.add(indices[i])
        edata = ""
        for i in range(len(data)):
            if i in s:
                edata += str((int(data[i])) ^ 1)
            else:
                edata += data[i]
        return edata
    @classmethod
    def oddBurstError(cls, data):
        n = len(data)
        # n = 31
        indices = [i for i in range(n)]
        # shuffle
        for i in range(n):
            swapind = randint(i, n - 1)
            indices[i], indices[swapind] = indices[swapind], indices[i]
        m = 0
        while m % 2 == 0:
            m = randint(1, n)
        s = set()
        for i in range(m):
            s.add(indices[i])
        edata = ""
        for i in range(len(data)):
            if i in s:
                edata += str((int(data[i])) ^ 1)
            else:
                edata += data[i]
        return edata
    @classmethod
    def injectError(cls, data):
        methods = [cls.singleError, cls.completeBurstError, cls.burstError]
        index = randint(0, 2)
        # return cls.oddBurstError(data)
        return methods[index](data)

