import string
import random
import re

n = 23 * (32 *13)

print(n)

print(type(string.printable))
res = ''.join(random.choices(re.sub(r'\s+', '',string.printable), k = n))
# print(res)

file = open("test.txt", "w")
file.write(res)
file.close()