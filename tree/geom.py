
import numpy as np


def buffers(root):
    # Add (a, b, c) in t, then recurse on all subdivisions and repeat.
    print(root.depth)
    print(root.faces)
    verts = np.zeros(shape=(root.faces*30, 2), dtype=np.float32)
    for i, v in enumerate(root):
        verts[i, :] = v
    return verts


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
        # Think this is depth-first traversal.
        for x in [self.a, self.b, self.c]:
            yield x
            if self.divs is not None:
                for sub in self.divs:
                    for y in sub:
                        yield y


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
        for x in [self.a, self.b, self.c, self.m]:
            yield x
