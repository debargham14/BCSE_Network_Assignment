import string
import random
import re
n = 13 * (32 ** 3)
res = ''.join(random.choices(re.sub(r'\s+', '',string.printable), k = n))

file = open("test.txt", "w")
file.write(res)
file.close()