import matplotlib.pyplot as plt
from Vertex import *
from VertexNormal import *
from Face import *

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



    def get2D(self, plane):
        # if x.z < 0.12
        # if x.z < 0.12
        # if x.z < 0.12

        if len(plane) != 2 or plane not in ["xy","yz","xz"]:
            raise Exception("Invalid plane.\n\tValid planes are [\"xy\",\"yz\",\"xz\"")

        xs = [x.x for x in self.vertices]
        ys = [x.y for x in self.vertices]
        zs = [x.z for x in self.vertices]

        fig = plt.figure()

        if plane == "xy":
            plt.scatter(xs, ys, c=zs, s=100, cmap='gray')
        elif plane == "yz":
            plt.scatter(ys, zs, c=xs, s=100, cmap='gray')
        elif plane == "xz":
            plt.scatter(xs, zs, c=ys, s=100, cmap='gray')

        def onclick(event):
            print event.x
            print event.y

        cid = fig.canvas.mpl_connect('button_press_event', onclick)

        plt.show()

        fig.canvas.mpl_disconnect(cid)

    def drawXY(self):
        xs = [x.x for x in self.vertices]
        ys = [x.y for x in self.vertices]
        zs = [x.z for x in self.vertices]

    def printStats(self):
        print "Total vertices: " + str(len(self.vertices))
        print "Total vertnorms: " + str(len(self.vertexNormals))
        print "Total faces: " + str(len(self.faces))
        print "Bounding Box:"
        print "\tX: " + str(self.minx) + " " + str(self.maxx)
        print "\tY: " + str(self.miny) + " " + str(self.maxy)
        print "\tZ: " + str(self.minz) + " " + str(self.maxz)
