
import numpy as np


def bottom(root):
    """
    Generate opengl buffers for only the triangles at the bottom of the tree.
    """
    l = root.final*3
    verts = np.zeros(shape=(l, 2), dtype=np.float32)
    index = np.zeros(shape=(l   ), dtype=np.uint32)
    color = np.zeros(shape=(l, 3), dtype=np.float32)
    i = 0
    for face in root.bottom():
        j = i*3
        color[j+0, :] = face.color
        color[j+1, :] = face.color
        color[j+2, :] = face.color
        index[j:j+3] = j+0, j+1, j+2
        verts[j+0, :] = face.a
        verts[j+1, :] = face.b
        verts[j+2, :] = face.c
        i += 1
    return verts, index, color


def buffers(root):
    """
    Generate opengl buffers for every triangle in the hierarchy, including
    larger divisions.
    """
    l = root.faces*3
    verts = np.zeros(shape=(l, 2), dtype=np.float32)
    index = np.zeros(shape=(l   ), dtype=np.uint32)
    color = np.zeros(shape=(l, 3), dtype=np.float32)
    i = 0
    for face in root.traverse():
        j = i*3
        r = np.random.random(3)
        color[j+0, :] = r
        color[j+1, :] = r
        color[j+2, :] = r
        index[j:j+3] = j+0, j+1, j+2
        verts[j+0, :] = face.a
        verts[j+1, :] = face.b
        verts[j+2, :] = face.c
        i += 1
    return verts, index, color


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


def vary(c, point, d=0.2):
    if point == 'a':
        return (c[0]+d, c[1], c[2])
    elif point == 'b':
        return (c[0], c[1]+d, c[2])
    elif point == 'c':
        return (c[0], c[1], c[2]+d)
    elif point == 'm':
        return c


class Triangle:
    def __init__(self, a, b, c, depth=0, color=(0.2, 0.2, 0.2)):
        """
        A subdividing triangle. Arguments are (x, y) pairs for each of the three
        corners.
        """
        self.a = a
        self.b = b
        self.c = c
        self.depth = depth
        self.color = color
        self.faces = sum(4**level for level in range(0, depth+1))
        self.final = 4**depth
        if depth > 0:
            self.divs = Division(self, depth-1, color)
        else:
            self.divs = None

    def __iter__(self):
        """
        Get each vertex pair in this triangle.
        """
        for x in [self.a, self.b, self.c]:
            yield x

    def __contains__(self, point):
        """
        Use barycentric coordinates to check if a point lies within the bounds
        of this triangle.
        """
        ax, ay = self.a
        bx, by = self.b
        cx, cy = self.c
        px, py = point
        div = ((ax * by) - (ax * cy) - (bx * ay) + (bx * cy) + (cx * ay) - (cx * by))
        #((X1 * Y2) - (X1 * Y3) - (X2 * Y1) + (X2 * Y3) + (X3 * Y1) - (X3 * Y2))
        u = ((px * by) - (px * cy) - (bx * py) + (bx * cy) + (cx * py) - (cx * by)) / div
        #((X4 * Y2) - (X4 * Y3) - (X2 * Y4) + (X2 * Y3) + (X3 * Y4) - (X3 * Y2))
        v = ((ax * py) - (ax * cy) - (px * ay) + (px * cy) + (cx * ay) - (cx * py)) / div
        #((X1 * Y4) - (X1 * Y3) - (X4 * Y1) + (X4 * Y3) + (X3 * Y1) - (X3 * Y4))
        w = ((ax * by) - (ax * py) - (bx * ay) + (bx * py) + (px * ay) - (px * by)) / div
        #((X1 * Y2) - (X1 * Y4) - (X2 * Y1) + (X2 * Y4) + (X4 * Y1) - (X4 * Y2))
        #print("U:", u)
        #print("W:", w)
        #print("V:", v)
        return all([u > 0, v > 0, w > 0])

    def locate(self, point):
        """
        Traverse the hierarchy until the smallest triangle containing a
        certain point is found.
        """
        if point in self:
            if self.divs is None:
                return self
            else:
                for tri in self.divs:
                    found = tri.locate(point)
                    if found is not None:
                        return found
        else:
            return None

    def traverse(self):
        """
        Iterate over every triangle in the tree, including the triangles that
        hold each successively smaller level.
        """
        yield self
        if self.divs is not None:
            for tri in self.divs:
                for x in tri.traverse():
                    yield x

    def bottom(self):
        """
        Iterate over the triangles at the finest level. Does not include
        higher-level triangles.
        """
        if self.divs is None:
            yield self
        else:
            for tri in self.divs:
                for x in tri.bottom():
                    yield x


class Division:
    def __init__(self, t, depth, color):
        ab = midpoint(t.a, t.b)
        bc = midpoint(t.b, t.c)
        ca = midpoint(t.c, t.a)
        self.a = Triangle(t.a, ab, ca, depth, vary(color, 'a'))
        self.b = Triangle(ab, t.b, bc, depth, vary(color, 'b'))
        self.c = Triangle(ca, bc, t.c, depth, vary(color, 'c'))
        self.m = Triangle(ca, ab, bc, depth, vary(color, 'm'))

    def __iter__(self):
        for div in [self.a, self.b, self.c, self.m]:
            yield div
