
import numpy as np
import math
from copy import deepcopy

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


class Tri:
    def __init__(self, v1, v2, v3):
        # catches duplicate vertices
        assert len({v1, v2, v3}) == len([v1, v2, v3])
        self.verts = {v1, v2, v3}
        self.edges = {Edge(v1, v2), Edge(v2, v3), Edge(v3, v1)}

    def __iter__(self):
        for v in self.verts:
            yield v
        
    def __hash__(self):
        return sum([hash(v) for v in self.verts])

    def __repr__(self):
        return "Tri({}, {}, {})".format(*self.verts)

    def includes(self, v):
        return v in self.verts

    def connects(self, v):
        try:
            i = self.verts.index(v)
        except ValueError:
            return False
        else:
            return self.verts[i]


def distance(v1, v2):
    return abs(v1-v2)


def median(v1, v2, weight=1):
    return ((v1*weight)+v2)/(weight+1)


class Geometry:
    def __init__(self):
        self.verts = set()
        self.edges = set()
        self.faces = set()

    def add_face(self, v1, v2, v3):
        self.faces.add(Tri(v1, v2, v3))
        self.edges.add(Edge(v1, v2))
        self.edges.add(Edge(v2, v3))
        self.edges.add(Edge(v3, v1))
        self.verts.add(v1)
        self.verts.add(v2)
        self.verts.add(v3)

    def add_edge(self, v1, v2):
        self.edges.add(Edge(v1, v2))
        self.verts.add(v1)
        self.verts.add(v2)

    def add_vert(self, v1):
        self.verts.add(v1)

    def triangles(self):
        v_count = 0
        i_count = 0
        verts = np.zeros(shape=(len(self.faces)*3, 3), dtype=np.float32)
        index = np.zeros(shape=(len(self.faces), 3), dtype=np.uint32)
        lines = np.zeros(shape=(len(self.faces)*3, 2), dtype=np.uint32)
        for v1, v2, v3 in self.faces:
            i1, i2, i3 = v_count, v_count+1, v_count+2
            verts[i1, :] = tuple(v1)
            verts[i2, :] = tuple(v2)
            verts[i3, :] = tuple(v3)
            index[i_count] = (i1, i2, i3)
            lines[i1] = (i1, i2)
            lines[i2] = (i2, i3)
            lines[i3] = (i3, i1)
            v_count += 3
            i_count += 1
        return verts, index, lines

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


def icosphere():
    t = ((1.0 + np.sqrt(5.0))) / 2.0
    verts = [
        (-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0),  # red
        (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),  # green
        (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1),  # blue
    ]
    faces = [
        (0, 11, 5),
        (0, 5, 1),
        (0, 1, 7),
        (0, 7, 10),
        (0, 10, 11),
        (1, 5, 9),
        (5, 11, 4),
        (11, 10, 2),
        (10, 7, 6),
        (7, 1, 8),
        (3, 9, 4),
        (3, 4, 2),
        (3, 2, 6),
        (3, 6, 8),
        (3, 8, 9),
        (4, 9, 5),
        (2, 4, 11),
        (6, 2, 10),
        (8, 6, 7),
        (9, 8, 1),
    ]
    ico = Geometry()
    for i1, i2, i3 in faces:
        x1, y1, z1 = verts[i1]
        x2, y2, z2 = verts[i2]
        x3, y3, z3 = verts[i3]
        v1, v2, v3 = Vert(x1, y1, z1), Vert(x2, y2, z2), Vert(x3, y3, z3)
        v1, v2, v3 = normalize(v1), normalize(v2), normalize(v3)
        ico.add_face(v1, v2, v3)
    return ico

def near(v, a, b, c):
    d = {m:sum(distance(v, m)) for m in [a, b, c]}
    l = sorted(d.items(), key=lambda x: x[1])
    return l[0][0], l[1][0]

def refine(old, norm=True):
    new = Geometry()
        
    for face in old.faces:
        midpoints = []
        e1, e2, e3 = face.edges
        m1 = median(e1.v1, e1.v2)
        m2 = median(e2.v1, e2.v2)
        m3 = median(e3.v1, e3.v2)
        if norm:
            m1 = normalize(m1)
            m2 = normalize(m2)
            m3 = normalize(m3)
        #new.add_face(e1.v1, m1, m2)
        #new.add_face(e2.v1, m2, m3)
        #new.add_face(e3.v1, m3, m1)
        new.add_face(e1.v1, *near(e1.v1, m1, m2, m3))
        new.add_face(e2.v1, *near(e2.v1, m1, m2, m3))
        new.add_face(e3.v1, *near(e3.v1, m1, m2, m3))
        new.add_face(m1, m2, m3)
    return new


def truncate(ico):
    new = deepcopy(old)
    for face in old.faces:
        midpoints = []
        for edge in face.edges:
            m1 = median(edge.v1, edge.v2, weight=2)
            m2 = median(edge.v2, edge.v1, weight=2)
            midpoints.append(m1)
            midpoints.append(m2)
        (ma, mb, mc) = midpoints
    return new


def normalize(v):
    mag = math.sqrt(sum(v*v))
    return v/mag
