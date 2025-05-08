import random
import string


def z(n):
    print("".join(random.choices(string.ascii_letters, k=n)))
    
