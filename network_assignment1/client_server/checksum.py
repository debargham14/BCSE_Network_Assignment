class CHECKSUM:
    @classmethod
    def binSum(cls, chunk1,chunk2,div=4):
    
        st=bin(int(chunk1,2)+int(chunk2,2))
        
        if len(st)==div+3:   #for removing first 0b from binay code 0bxxxxxx
            carry='1'
            st1=st[3:]
            st= cls.binSum(st1,carry)
            return st
        else:
            return st[2:]
        
    @classmethod
    def findCheckSum(cls, message,div):
        mess_len=len(message)
            
        temp=message[:div]
        message=message[div:]

        for i in range((mess_len//div)-1):
            temp=cls.binSum(temp,message[:div])
            message=message[div:]

        checkSum=temp

        #for taking compliment of check_sum
        for i in range(len(checkSum)):
            if checkSum[i]=='0':
                checkSum=checkSum[:i]+'1'+checkSum[i+1:]
            else:
                checkSum=checkSum[:i]+'0'+checkSum[i+1:]
                    
        return checkSum

