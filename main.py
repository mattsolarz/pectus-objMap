import sys
import matplotlib.pyplot as plt

# classes
class Vertex(object):

    def __init__(self, x, y , z):
        self.x = x
        self.y = y
        self.z = z

class VertexNormal(object):

    def __init__(self, xn, yn, zn):
        self.xn = xn
        self.yn = yn
        self.zn = zn

class Face(object):

    def __init__(self, v1, vn1, v2, vn2, v3, vn3):
        self.v1  = v1
        self.vn1 = vn1

        self.v2  = v2
        self.vn2 = vn2

        self.v3  = v3
        self.vn3 = vn3

class Model(object):

    def __init__(self, filename):
        # init the points
        self.vertices = []
        self.vertexNormals = []
        self.faces = []

        # init the bounding box
        self.minx, self.miny, self.minz = 99999,99999,99999
        self.maxx, self.maxy, self.maxz = -99999, -99999, -99999

        # init the filename
        self.filename = filename

        # populate it all
        self.readIn()

    def readIn(self):
        with open(self.filename) as f:
            content = f.readlines()

        content = [x.strip("\n") for x in content]

        for c in content:
            if len(c) > 0 and c[0] == '#':
                # It's a comment, ignore it
                continue

            line = c.split(' ')

            if len(line) < 2:
                # TODO: maybe throw an error?
                continue

            if line[0] == "v":
                # Vertex
                x = float(line[1])
                y = float(line[2])
                z = float(line[3])

                self.vertices.append(Vertex(x, y, z))

                # Figure out bounding boxes
                if x < self.minx:
                    self.minx = x
                if x > self.maxx:
                    self.maxx = x
                if y < self.miny:
                    self.miny = y
                if y > self.maxy:
                    self.maxy = y
                if z < self.minz:
                    self.minz = z
                if z > self.maxz:
                    self.maxz = z

            elif line[0] == "vn":
                # Vector normal

                if line[1] == "nan" or line[2] == "nan" or line[3] == "nan":
                    self.vertexNormals.append(VertexNormal(0,0,0))

                self.vertexNormals.append(VertexNormal(float(line[1]), float(line[2]), float(line[3])))
            elif line[0] == "f":
                # Face
                x = line[1].split('/')
                y = line[2].split('/')
                z = line[3].split('/')

                if len(x) < 3 or len(y) < 3 or len(z) < 3:
                    raise Exception("Invalid Face Format")

                self.faces.append(Face(x[0],x[2],y[0],y[2],z[0],z[2]))

    def flip(self, flipx, flipy, flipz):
        for i in range(len(self.vertices)):
            if flipx:
                self.vertices[i].x = self.maxx - self.vertices[i].x
            if flipy:
                self.vertices[i].y = self.maxy - self.vertices[i].y
            if flipz:
                self.vertices[i].z = self.maxz - self.vertices[i].z

        self.calculateBounding()

    def calculateBounding(self):
        self.minx, self.miny, self.minz = 99999,99999,99999
        self.maxx, self.maxy, self.maxz = -99999, -99999, -99999

        for v in self.vertices:
            x = v.x
            y = v.y
            z = v.z

            if x < self.minx:
                self.minx = x
            if x > self.maxx:
                self.maxx = x
            if y < self.miny:
                self.miny = y
            if y > self.maxy:
                self.maxy = y
            if z < self.minz:
                self.minz = z
            if z > self.maxz:
                self.maxz = z



    def get2D(self):
        xs = [x.x for x in self.vertices if x.z < 0.12]
        ys = [x.y for x in self.vertices if x.z < 0.12]
        zs = [x.z for x in self.vertices if x.z < 0.12]

        fig = plt.figure()

        #ax = plt.add_subplot(111)

        plt.scatter(xs, ys, c=zs, s=100, cmap='gray')

        def onclick(event):
            print event.x
            print event.y

        cid = fig.canvas.mpl_connect('thing', onclick)

        plt.show()

    def printStats(self):
        print "Total vertices: " + str(len(self.vertices))
        print "Total vertnorms: " + str(len(self.vertexNormals))
        print "Total faces: " + str(len(self.faces))
        print "Bounding Box:"
        print "\tX: " + str(self.minx) + " " + str(self.maxx)
        print "\tY: " + str(self.miny) + " " + str(self.maxy)
        print "\tZ: " + str(self.minz) + " " + str(self.maxz)


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

    model.get2D()

main()
