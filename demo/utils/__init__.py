import random
import string

def randchars(length):
  return "".join(random.choice(string.letters) \
      for _ in range(0, length))


