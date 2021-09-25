class CRC:
    @classmethod
    def xor(cls, a, b):
        #initialising the result
        result = []
        for i in range (1, len(b)):
            if a[i] == b[i]:
                result.append ('0')
            else:
                result.append ('1')
        return ''.join(result)

    # Performs Modulo-2 divisior
    @classmethod
    def mod2div(cls, divident, divisor):
    
        # Number of bits to be XORed at a time.
        pick = len(divisor)
    
        # Slicing the divident to appropriate
        # length for particular step
        tmp = divident[0 : pick]
    
        while pick < len(divident):
    
            if tmp[0] == '1':
    
                # replace the divident by the result
                # of XOR and pull 1 bit down
                tmp = cls.xor(divisor, tmp) + divident[pick]
    
            else:  
                tmp = cls.xor('0'*pick, tmp) + divident[pick]
    
            # increment pick to move further
            pick += 1
    
        if tmp[0] == '1':
            tmp = cls.xor(divisor, tmp)
        else:
            tmp = cls.xor('0'*pick, tmp)
    
        checkword = tmp
        return checkword
    @classmethod
    def encodeData(cls, data, key):
    
        l_key = len(key)
    
        # Appends n-1 zeroes at end of data
        appended_data = data + '0'*(l_key-1)
        remainder = cls.mod2div(appended_data, key)
    
        # Append remainder in the original data
        codeword = data + remainder
        return codeword
    @classmethod
    def returnRemainder (cls, data, key):
        l_key = len(key)
    
        # Appends n-1 zeroes at end of data
        appended_data = data + '0'*(l_key-1)
        remainder = cls.mod2div(appended_data, key)
    
        return remainder