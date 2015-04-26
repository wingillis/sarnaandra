import numpy
import random
import os
import time
path = '~'

path = os.path.expanduser(path)

path = os.path.join(path, 'Desktop', 'testing3')

extension = 'dat'
counter = 0
fs = 600
if not os.path.exists(path):
    os.makedirs(path)

if __name__ == '__main__':
    while True:
        t = numpy.linspace(0, 1, 1*fs)
        sin_frequency = random.randint(1, 100)  # hopefully in Hz
        w = 2. * numpy.pi * sin_frequency
        v = 2. * numpy.sin(w*t)
        filename = '{0}_{1}.{2}'.format(sin_frequency, counter, extension)
        counter += 1

        with open(os.path.join(path, filename), 'w') as f:
            t = map(str, t)
            v = map(str, v)
            f.write(','.join(t))
            f.write('\n')
            f.write(','.join(v))
            print('wrote file {0}'.format(filename))
        time.sleep(15)
