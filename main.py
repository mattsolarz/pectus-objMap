import sys
from Model import *
import matplotlib.pyplot as plt
#import enaml
#from enaml.qt.qt_application import QtApplication

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

    model.flip(flipx, flipy, flipz)

    constraints = model.get2D("xy")

    slice = model.sliceY(constraints[0][1])

    xs = [x[0] for x in slice]
    zs = [x[1] for x in slice]

    plt.scatter(xs, zs)
    plt.show()

    #model.constrain("x",constraints[0][0],constraints[1][0])

    #c2 = model.get2D("xz")

    #model.constrain("z",c2[0][1],c2[1][1])

    #model.drawConstraints("xy")

if __name__ == '__main__':
    main()