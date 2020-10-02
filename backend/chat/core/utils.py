from string import ascii_letters
import random


def random_string(length=10):
    return ''.join(random.choices(ascii_letters, k=length))