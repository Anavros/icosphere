
import numpy as np
import math
from copy import deepcopy
import random

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


class Face:
    def __init__(self, *args):
        self.verts = args
    def __iter__(self):
        for v in self.verts:
            yield v
    def __hash__(self):
        return sum([hash(v) for v in self.verts])
    def __len__(self):
        return len(self.verts)


def distance(v1, v2):
    return abs(v1-v2)


def median(v1, v2, weight=1):
    return ((v1*weight)+v2)/(weight+1)


def center(v1, v2, v3):
    return (v1+v2+v3)/3


class Geometry:
    def __init__(self):
        #self.verts = set()
        #self.edges = set()
        self.faces = set()

        self.counts = {}
        self.n_triangles = 0
        self.n_verts = 0

    def add(self, *args):
        n = len(args)
        try:
            self.counts[n] += 1
        except KeyError:
            self.counts[n] = 1
        self.n_triangles += (1 if n==3 else 2 if n==4 else n)
        self.n_verts += n
        self.faces.add(Face(*args))

    def triangles(self):
        v_count = 0
        i_count = 0
        verts = np.zeros(shape=(self.n_verts, 3), dtype=np.float32)
        index = np.zeros(shape=(self.n_triangles, 3), dtype=np.uint32)
        lines = np.zeros(shape=(self.n_verts, 2), dtype=np.uint32)
        for face in self.faces:
            if len(face) == 3:
                v1, v2, v3 = face.verts
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
            else:
                raise ValueError("Weird face! {} sides!".format(len(face)))
        return verts, index, lines


def icosphere():
    t = ((1.0 + np.sqrt(5.0))) / 2.0
    verts = [
        (-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0),
        (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
        (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1),
    ]
    faces = [
        (0, 11, 5), (0, 5, 1),
        (0, 1, 7), (0, 7, 10),
        (0, 10, 11), (1, 5, 9),
        (5, 11, 4), (11, 10, 2),
        (10, 7, 6), (7, 1, 8),
        (3, 9, 4), (3, 4, 2),
        (3, 2, 6), (3, 6, 8),
        (3, 8, 9), (4, 9, 5),
        (2, 4, 11), (6, 2, 10),
        (8, 6, 7), (9, 8, 1),
    ]
    ico = Geometry()
    for i1, i2, i3 in faces:
        x1, y1, z1 = verts[i1]
        x2, y2, z2 = verts[i2]
        x3, y3, z3 = verts[i3]
        v1, v2, v3 = Vert(x1, y1, z1), Vert(x2, y2, z2), Vert(x3, y3, z3)
        v1, v2, v3 = normalize(v1), normalize(v2), normalize(v3)
        ico.add(v1, v2, v3)
    return ico


def refine(old, norm=True):
    new = Geometry()
    for face in old.faces:
        v1, v2, v3 = face.verts
        m1 = median(v1, v2)
        m2 = median(v2, v3)
        m3 = median(v3, v1)
        if norm:
            m1 = normalize(m1, 1)
            m2 = normalize(m2, 1)
            m3 = normalize(m3, 1)
        new.add(v1, *near(v1, m1, m2, m3))
        new.add(v2, *near(v2, m1, m2, m3))
        new.add(v3, *near(v3, m1, m2, m3))
        new.add(m1, m2, m3)
    return new


def extrude(old):
    new = Geometry()
    for face in old.faces:
        v1, v2, v3 = face.verts
        if random.uniform(0, 1) < 0.5:
            delta = random.choice([1.2, 1.3, 1.5])
            d1, d2, d3 = normalize(v1, delta), normalize(v2, delta), normalize(v3, delta)
            #new.add(v1, v2, v3)
            new.add(d1, d2, d3)

            new.add(v1, d1, v2)
            new.add(d2, d1, v2)
            new.add(v2, d2, v3)
            new.add(d3, d2, v3)
            new.add(v3, d3, v1)
            new.add(d1, d3, v1)
        else:
            new.add(v1, v2, v3)
    return new


def truncate(old):
    new = Geometry()
    for face in old.faces:
        v1, v2, v3 = face.verts
        
        cen = center(face.v1, face.v2, face.v3)
        m1a = median(v1, v2, weight=2)
        m1b = median(v2, v1, weight=2)
        m2a = median(v2, v3, weight=2)
        m2b = median(v3, v2, weight=2)
        m3a = median(v3, v1, weight=2)
        m3b = median(v1, v3, weight=2)

        new.add(cen, m1a, m1b, m2a, m2b, m3a, m3b)

        new.add_face(e1.v1, *near(e1.v1, m1a, m1b, m2a, m2b, m3a, m3b))
        new.add_face(e2.v1, *near(e2.v1, m1a, m1b, m2a, m2b, m3a, m3b))
        new.add_face(e3.v1, *near(e3.v1, m1a, m1b, m2a, m2b, m3a, m3b))
        new.add_face(cen, m1a, m1b)
        new.add_face(cen, m2a, m2b)
        new.add_face(cen, m3a, m3b)

        #new.add_face(cen, m1a, m2b)
        #new.add_face(cen, m2a, m3b)
        #new.add_face(cen, m3a, m1b)
    return new


def normalize(v, height=1):
    l = math.sqrt(sum(v*v))
    return (v*height)/l

def near(v, *args):
    d = {m:sum(distance(v, m)) for m in args}
    l = sorted(d.items(), key=lambda x: x[1])
    return l[0][0], l[1][0]
