import sys
from Model import *
import enaml
from enaml.qt.qt_application import QtApplication

def main():
    argc = len(sys.argv)

    if argc < 2:
        print "error"
        exit(1)

    flipx = False
    flipy = False
    flipz = False

    args = []

    for i in range(2, argc):
        args.append(sys.argv[i])

    if "x" in args:
        flipx = True
    if "y" in args:
        flipy = True
    if "z" in args:
        flipz = True

    print "Beginning read of " + sys.argv[1]

    # get filename
    filename = sys.argv[1]

    model = Model(filename)

    model.printStats()

    model.flip(flipx, flipy, flipz)

    model.printStats()

    model.get2D("xy")

if __name__ == '__main__':
    main()