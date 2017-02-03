
import numpy as np


def buffers(root):
    # Add (a, b, c) in t, then recurse on all subdivisions and repeat.
    #print(root.depth)
    #print(root.faces)
    verts = np.zeros(shape=(root.faces*3, 2), dtype=np.float32)
    i = 0
    for face in root.traverse():
        verts[i+0, :] = face.a
        verts[i+1, :] = face.b
        verts[i+2, :] = face.c
        i += 3
    print(verts)
    return verts


def count(root):
    i = 0
    for tri in root.traverse():
        print("Verts:", tri.a, tri.b, tri.c)
        print("Depth:", tri.depth)
        print("Faces:", tri.faces)
        i += 1
    print("Total:", i)


def midpoint(a, b):
    ax, ay = a
    bx, by = b
    return (ax+bx)/2, (ay+by)/2


class Triangle:
    def __init__(self, a, b, c, depth=0):
        """
        A subdividing triangle. Arguments are (x, y) pairs for each of the three
        corners.
        """
        self.a = a
        self.b = b
        self.c = c
        self.depth = depth
        self.faces = sum(4**level for level in range(0, depth+1))
        if depth > 0:
            self.divs = Division(self, depth-1)
        else:
            self.divs = None

    def __iter__(self):
        for x in [self.a, self.b, self.c]:
            yield x

    def traverse(self):
        yield self
        if self.divs is not None:
            for tri in self.divs:
                for x in tri.traverse():
                    yield x


class Division:
    def __init__(self, t, depth):
        ab = midpoint(t.a, t.b)
        bc = midpoint(t.b, t.c)
        ca = midpoint(t.c, t.a)
        self.a = Triangle(t.a, ab, ca, depth)
        self.b = Triangle(ab, t.b, bc, depth)
        self.c = Triangle(ca, bc, t.c, depth)
        self.m = Triangle(ca, ab, bc, depth)

    def __iter__(self):
        for div in [self.a, self.b, self.c, self.m]:
            yield div
