import random
import string


def zowner(n):
    print("".join(random.choices(string.ascii_letters, n)))
    
