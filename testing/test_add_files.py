import string
import random
import os
import time
path = '~'

path = os.path.expanduser(path)

path = os.path.join(path, 'desktop', 'testing')

if not os.path.exists(path):
    os.makedirs(path)

if __name__ == '__main__':
    while True:
        letter_choice1 = random.choice(string.lowercase)
        letter_choice2 = random.choice(string.lowercase)
        ocurrences1 = random.randrange(100)
        ocurrences2 = random.randrange(100)
        filename = '{0}-{1}_{2}-{3}'.format(letter_choice1, ocurrences1,
                                            letter_choice2, ocurrences2)
        with open(os.path.join(path, filename), 'w') as f:
            f.write(letter_choice1*ocurrences1)
            f.write('\n')
            f.write(letter_choice2*ocurrences2)
        time.sleep(6)