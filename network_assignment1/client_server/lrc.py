class LRC_VRC:
    @classmethod
    def getParity(cls, message):
        parity = 0
        count1 = 0
        for i in range(0, len(message)):
            if message[i] == '1':
                count1 += 1

        if count1 % 2 == 0:
            return '0'
        else:
            return '1'
    @classmethod
    def calcLRC(cls, word):
        # Even parity
        words = []
        words.append (word[0:8])
        words.append (word[8:16])
        words.append (word[16:24])
        words.append(word[24:32])
        

        parity = ""
        subword = ""
        for i in range(0,len(words[0])):
            for j in range(0, len(words)):        
                subword += words[j][i]
            parity += cls.getParity(subword)
            subword = ""
        # print(parity)
        return parity
    @classmethod
    def calcVRC(cls, message):
        # Even parity
        return cls.getParity(message)
