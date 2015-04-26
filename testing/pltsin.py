import matplotlib.pyplot as plt
import os


def run(filename):
    lines = []
    base = os.path.basename(filename)
    fname, ext = os.path.splitext(base)
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line)

    x = lines[0].split(',')
    x = list(map(float, x))
    y = lines[1].split(',')
    y = list(map(float, y))
    plt.clf()
    plt.plot(x, y)
    newfname = fname + '.png'
    plt.savefig(newfname)
    return os.path.abspath(newfname)
