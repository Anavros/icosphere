
import numpy as np


def identity():
    return np.eye(4, dtype=np.float32)


def point():
    return np.array([
        (0.0, 0.0),
    ], dtype=np.float32)


def square():
    return np.array([
        (-0.2, +0.2), (+0.2, +0.2),
        (-0.2, -0.2), (+0.2, -0.2),
    ], dtype=np.float32)


def cube(x=1.0):
    return np.array([
        (-x, +x, +x), (+x, +x, +x),
        (-x, -x, +x), (+x, -x, +x),
        (-x, +x, -x), (+x, +x, -x),
        (-x, -x, -x), (+x, -x, -x),
    ], dtype=np.float32)


def cube_color():
    return np.array([
        (0, 0, 0), (0, 0, 0),
        (0, 0, 0), (0, 0, 0),
        (0, 0, 0), (0, 0, 0),
        (0, 0, 0), (0, 0, 0),
    ], dtype=np.float32)


class Vert:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        for n in [self.x, self.y, self.z]:
            yield n

    def __add__(self, x):
        if type(x) is Vert:  # for scalar operations / duck typed ops
            vert = x
        else:
            vert = Vert(x, x, x)
        return Vert(self.x+vert.x, self.y+vert.y, self.z+vert.z)

    def __sub__(self, x):
        if type(x) is Vert:
            vert = x
        else:
            vert = Vert(x, x, x)
        return Vert(self.x-vert.x, self.y-vert.y, self.z-vert.z)

    def __mul__(self, x):
        if type(x) is Vert:
            vert = x
        else:
            vert = Vert(x, x, x)
        return Vert(self.x*vert.x, self.y*vert.y, self.z*vert.z)

    def __truediv__(self, x):
        if type(x) is Vert:
            vert = x
        else:
            vert = Vert(x, x, x)
        return Vert(self.x/vert.x, self.y/vert.y, self.z/vert.z)

    def __abs__(self):
        return Vert(abs(self.x), abs(self.y), abs(self.z))

    def __sum__(self):
        return self.x+self.y+self.z

    def __eq__(self, vert):
        return self.x==vert.x and self.y==vert.y and self.z==vert.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        return "Vert({:.2f}, {:.2f}, {:.2f})".format(self.x, self.y, self.z)


class Edge:
    def __init__(self, v1, v2):
        assert type(v1) is Vert
        assert type(v2) is Vert
        self.v1 = v1
        self.v2 = v2

    def __iter__(self):
        for n in [self.v1, self.v2]:
            yield n

    def __eq__(self, edge):
        return ((self.v1==edge.v1 and self.v2==edge.v2) or
            (self.v1==edge.v2 and self.v2==edge.v1))

    def __hash__(self):
        return hash(self.v1)+hash(self.v2)

    def __repr__(self):
        return "{} <-> {}".format(self.v1, self.v2)

    def includes(self, v):
        return v in [self.v1, self.v2]

    def connects(self, v):
        if v == self.v1:
            return self.v2
        elif v == self.v2:
            return self.v1
        else:
            return False


def distance(v1, v2):
    return abs(v1-v2)


def median(v1, v2, weight=1):
    return ((v1*weight)+v2)/(weight+1)


class Geometry:
    def __init__(self):
        self.edges = set()

    def data(self):
        v_count = 0
        i_count = 0
        verts = np.zeros(shape=(len(self.edges)*2, 3), dtype=np.float32)
        index = np.zeros(shape=(len(self.edges), 2), dtype=np.uint32)
        for v1, v2 in self.edges:
            i1, i2 = v_count, v_count+1
            verts[i1, :] = tuple(v1)
            verts[i2, :] = tuple(v2)
            index[i_count] = (i1, i2)
            v_count += 2
            i_count += 1
        return verts, index

    def adjacent_to(self, v):
        return [e.connects(v) for e in self.edges if e.includes(v)]

    def vertices(self):
        return set([v for e in self.edges for v in list(e)])

    def cull(self, v):
        self.edges = self.edges - set([e for e in self.edges if e.includes(v)])

    def cull_all(self, vs):
        for v in vs:
            self.cull(v)

    def connect(self, v1, v2):
        self.edges.add(Edge(v1, v2))

    def connect_all(self, verts, limit=None):
        for v1 in verts:
            for v2 in verts:
                if v1==v2: continue
                if not limit:
                    self.connect(v1, v2)
                else:
                    (dx, dy, dz) = distance(v1, v2)
                    if all([dx<limit, dy<limit, dz<limit]):
                        self.connect(v1, v2)

def refine(icosphere):
    new = Geometry()
    new.edges = icosphere.edges
    midpoints = []
    for v1 in new.vertices():
        for v2 in new.adjacent_to(v1):
            m = median(v1, v2)
            new.connect(m, v1)
            midpoints.append(m)
    new.connect_all(midpoints, limit=1.1)
    return new


def truncate(icosphere):
    new = Geometry()
    old_verts = icosphere.vertices()
    for v1 in old_verts:
        ms = []
        for v2 in icosphere.adjacent_to(v1):
            m1 = median(v1, v2, 2)
            m2 = median(v2, v1, 2)
            ms.append(m1)
            new.connect(m1, m2)
        for m1 in ms:
            for m2 in ms:
                (dx, dy, dz) = tuple(distance(m1, m2))
                if dx==0 and dy==0 and dz==0: continue
                if all([
                    dx < 0.4,
                    dy < 0.4,
                    dz < 0.4,
                ]):
                    new.connect(m1, m2)
        del ms
    new.cull_all(old_verts)
    return new


def iterate(icosphere):
    new = Geometry()
    for v1 in icosphere.vertices():
        for v2 in icosphere.adjacent_to(v1):
            m1 = median(v1, v2)
            new.connect(m1, v1)
            for va in icosphere.adjacent_to(v2):
                for vb in icosphere.adjacent_to(v2):
                    m2 = median(va, vb)
                    #new.connect(m2, va)
    return new


def icosphere():
    t = ((1.0 + np.sqrt(5.0))) / 2.0
    verts = [
        (-1, t, 0), (1, t, 0), (1, -t, 0), (-1, -t, 0),  # red
        (0, -1, t), (0, 1, t), (0, 1, -t), (0, -1, -t),  # green
        (t, 0, -1), (t, 0, 1), (-t, 0, 1), (-t, 0, -1),  # blue
    ]
    edges = [
        (0, 1),
        (2, 3),
        (4, 5),
        (6, 7),
        (8, 9),
        (10, 11),
        (0, 5),
        (1, 5),
        (0, 6),
        (1, 6),
        (2, 7),
        (3, 7),
        (2, 4),
        (3, 4),
        (0, 10),
        (0, 11),
        (3, 10),
        (3, 11),
        (1, 8),
        (1, 9),
        (2, 8),
        (2, 9),
        (4, 10),
        (4, 9),
        (5, 10),
        (5, 9),
        (6, 8),
        (6, 11),
        (7, 8),
        (7, 11),
    ]
    geo = Geometry()
    for v1, v2 in edges:
        x1, y1, z1 = verts[v1]
        x2, y2, z2 = verts[v2]
        geo.connect(Vert(x1, y1, z1), Vert(x2, y2, z2))
    return geo
