import random

class InjectError:
    @classmethod
    def singleError (cls, data):
        idx = random.randint(0, len(data) - 1)
        temp = list(data)
        if(data[idx] == '1'):
            temp[idx] = '0'
        else:
            temp[idx] = '1'
        return ''.join(temp)
    @classmethod 
    def burstError (cls, data):
        l, r = 3,5
        temp = list(data)
        for i in range (l, r):
            if (data[i] == '1'):
                temp[i] = '0'
            else:
                temp[i] = '1'
        return ''.join(temp)

    @classmethod
    def multipleError (cls, data):
        temp = list(data)
        for i in range (0, len(data)):
            idx = random.randint(i, len(data) - 1)
            if (data[idx] == '0'):
                temp[idx] = '1'
            else:
                temp[idx] = '0'
        return ''.join(temp)
