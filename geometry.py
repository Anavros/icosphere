
import numpy as np
import math
from copy import deepcopy
import random
import itertools

#from polyhedra import Vert, Edge, Face, Triangle, Pentagon, Hexagon
# traverse once for every vertex
# get all edges
# make a vertex 1/3 of the way down
# and make a new face using all of the new vertices
# traverse once for every face (triangle)
# get edges
# make 6 points, 2 for each edge
# use those points to make a hexagon
# but then how to maintain order?

class Vert:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __iter__(self):
        for n in [self.x, self.y, self.z]:
            yield n
    def __add__(self, x):
        vert = x if type(x) is Vert else Vert(x, x, x)
        return Vert(self.x+vert.x, self.y+vert.y, self.z+vert.z)
    def __sub__(self, x):
        vert = x if type(x) is Vert else Vert(x, x, x)
        return Vert(self.x-vert.x, self.y-vert.y, self.z-vert.z)
    def __mul__(self, x):
        vert = x if type(x) is Vert else Vert(x, x, x)
        return Vert(self.x*vert.x, self.y*vert.y, self.z*vert.z)
    def __truediv__(self, x):
        vert = x if type(x) is Vert else Vert(x, x, x)
        return Vert(self.x/vert.x, self.y/vert.y, self.z/vert.z)
    def __abs__(self):
        return Vert(abs(self.x), abs(self.y), abs(self.z))
    def __sum__(self):
        return self.x+self.y+self.z
    def __eq__(self, vert):
        #ep = 0.001
        #dx = abs(self.x-vert.x)
        #dy = abs(self.y-vert.y)
        #dz = abs(self.z-vert.z)
        #return dx < ep and dy < ep and dz < ep
        return self.x==vert.x and self.y==vert.y and self.z==vert.z
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    def __repr__(self):
        return "Vert({:.2f}, {:.2f}, {:.2f})".format(self.x, self.y, self.z)
    def normalize(self):
        length = math.sqrt(sum(self*self))
        return Vert(self.x, self.y, self.z)/length


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
    def __init__(self, *args, tags=None):
        self.verts = args
        self.tags = tags if tags is not None else []
    def __iter__(self):
        for v in self.verts:
            yield v
    def __hash__(self):
        return sum([hash(v) for v in self.verts])
    def __len__(self):
        return len(self.verts)
    def shared(self, other_face):
        return set(self.verts) & set(other_face.verts)


class Triangle(Face):
    pass

class Pentagon(Face):
    pass

class Hexagon(Face):
    pass

class HexPlanet():
    def __init__(self, refine=0, force_refine=False):
        self.hexes = set()
        self.pents = set()
        self.adjacents = {}
        self.neighbors = set()

        t = ((1.0 + np.sqrt(5.0))) / 2.0
        verts = [
            (-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0),
            (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
            (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1),
        ]
        faces = [
            (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), # top
            (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8), # side
            (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), # bottom
            (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1), # side
        ]
        pents = [
            (0, 11, 5, 1, 7, 10), # top
            (3, 4, 2, 6, 8, 9), # bottom
            (11, 0, 5, 4, 2, 10),
            (5, 0, 1, 9, 4, 11),
            (1, 0, 7, 8, 9, 5),
            (7, 0, 1, 8, 6, 10),
            (10, 0, 11, 2, 6, 7),
            (4, 3, 2, 11, 5, 9),
            (2, 3, 6, 10, 11, 4),
            (6, 3, 8, 7, 10, 2),
            (8, 3, 9, 1, 7, 6),
            (9, 3, 4, 5, 1, 8),
        ]
        tags = [
            'draw_lines',
        ]
        connections = {
            0: [(0, 5, 11), (0, 5, 1)] # this is just repeating faces over again
        }
        moved = {}
        for ic, i1, i2, i3, i4, i5 in pents:
            v1 = Vert(*verts[i1]).normalize()
            v2 = Vert(*verts[i2]).normalize()
            v3 = Vert(*verts[i3]).normalize()
            v4 = Vert(*verts[i4]).normalize()
            v5 = Vert(*verts[i5]).normalize()
            cn = Vert(*verts[ic]).normalize()
            m1 = median(cn, v1, weight=2)
            m2 = median(cn, v2, weight=2)
            m3 = median(cn, v3, weight=2)
            m4 = median(cn, v4, weight=2)
            m5 = median(cn, v5, weight=2)
            mc = (m1+m2+m3+m4+m5)/5
            moved[cn] = mc
            #self.adjacents[mc] = {m1, m2, m3, m4, m5} these are just the pent verts
            #self.add_pen(v1, v2, v3, v4, v5, cn, tags)
            self.add_pen(m1, m2, m3, m4, m5, mc, tags)
        for i1, i2, i3 in faces:
            v1 = Vert(*verts[i1]).normalize()
            v2 = Vert(*verts[i2]).normalize()
            v3 = Vert(*verts[i3]).normalize()
            m1a = median(v1, v2, weight=2)
            m2a = median(v2, v3, weight=2)
            m3a = median(v3, v1, weight=2)
            m1b = median(v2, v1, weight=2)
            m2b = median(v3, v2, weight=2)
            m3b = median(v1, v3, weight=2)
            mc = (m1a+m2a+m3a+m1b+m2b+m3b)/6
            self.neighbors.add(Edge(mc, moved[v1]))
            self.neighbors.add(Edge(mc, moved[v2]))
            self.neighbors.add(Edge(mc, moved[v3]))
            # needs six connections!
            # other hexes need to connect to this one
            self.connect(mc, moved[v1], moved[v2], moved[v3])
            #self.adjacents[mc] = {moved[v1], moved[v2], moved[v3]}
            self.add_hex(m1a, m1b, m2a, m2b, m3a, m3b, mc, tags)


    def add_hex(self, v1, v2, v3, v4, v5, v6, center, tags=None):
        self.hexes.add(Hexagon(v1, v2, v3, v4, v5, v6, center, tags=tags))

    def add_pen(self, v1, v2, v3, v4, v5, center, tags=None):
        self.pents.add(Pentagon(v1, v2, v3, v4, v5, center, tags=tags))

    def get_hexes(self):
        return self.hexes

    def get_pents(self):
        return self.pents

    def get_all_faces(self):
        return list(self.hexes) + list(self.pents)

    def connect(self, *vecs):
        pass

    def refine(self):
        old_hexes = deepcopy(self.hexes)
        old_pents = deepcopy(self.pents)
        self.hexes = set()
        self.pents = set()
        moved = {}
        for h in old_hexes:
            ns = find_neighbors(old_hexes|old_pents, h)
            n1, n2, n3, n4, n5, n6 = arrange(ns)
            v1, v2, v3, v4, v5, v6, cn = h.verts 
            for w1, w2 in [(n1, n2), (n2, n3), (n3, n4), (n4, n5), (n5, n6), (n6, n1)]:
                m1a = median(cn, w1, weight=2)
                m2a = median(w1, w2, weight=2)
                m3a = median(w2, cn, weight=2)
                m1b = median(w1, cn, weight=2)
                m2b = median(w2, w1, weight=2)
                m3b = median(cn, w2, weight=2)
                mc = (m1a+m1b+m2a+m2b+m3a+m3b)/6
                # cache connection?
                self.add_hex(m1a, m1b, m2a, m2b, m3a, m3b, mc)
        for p in []:
            ns = find_neighbors(old_hexes|old_pents, p)
            n1, n2, n3, n4, n5 = arrange(ns)
            v1, v2, v3, v4, v5, cn = p.verts 
            for w1, w2 in [(n1, n2), (n2, n3), (n3, n4), (n4, n5), (n5, n1)]:
                m1a = median(cn, w1, weight=2)
                m2a = median(w1, w2, weight=2)
                m3a = median(w2, cn, weight=2)
                m1b = median(w1, cn, weight=2)
                m2b = median(w2, w1, weight=2)
                m3b = median(cn, w2, weight=2)
                mc = (m1a+m1b+m2a+m2b+m3a+m3b)/6
                self.add_pen(m1a, m1b, m2a, m2b, m3a, m3b, mc)

    def render(self):
        v_count = 0
        i_count = 0
        verts = np.zeros((len(self.hexes)*7 + len(self.pents)*6, 3), dtype=np.float32)
        index = np.zeros((len(self.hexes)*6 + len(self.pents)*5, 3), dtype=np.uint32)
        lines = np.zeros((len(self.hexes)*7 + len(self.pents)*6, 2), dtype=np.uint32)
        color = np.zeros((len(self.hexes)*7 + len(self.pents)*6, 3), dtype=np.float32)
        for h in self.get_hexes():
            c = np.random.random(3)
            v1, v2, v3, v4, v5, v6, cen = h.verts
            verts[v_count+0] = tuple(v1)
            verts[v_count+1] = tuple(v2)
            verts[v_count+2] = tuple(v3)
            verts[v_count+3] = tuple(v4)
            verts[v_count+4] = tuple(v5)
            verts[v_count+5] = tuple(v6)
            verts[v_count+6] = tuple(cen)
            color[v_count:v_count+7] = c

            index[i_count+0] = (v_count+6, v_count+0, v_count+1)
            index[i_count+1] = (v_count+6, v_count+1, v_count+2)
            index[i_count+2] = (v_count+6, v_count+2, v_count+3)
            index[i_count+3] = (v_count+6, v_count+3, v_count+4)
            index[i_count+4] = (v_count+6, v_count+4, v_count+5)
            index[i_count+5] = (v_count+6, v_count+5, v_count+0)

            lines[v_count+0] = (v_count+0, v_count+1)
            lines[v_count+1] = (v_count+1, v_count+2)
            lines[v_count+2] = (v_count+2, v_count+3)
            lines[v_count+3] = (v_count+3, v_count+4)
            lines[v_count+4] = (v_count+4, v_count+5)
            lines[v_count+5] = (v_count+5, v_count+0)
            v_count += 7
            i_count += 6
        for p in self.get_pents():
            c = np.random.random(3)
            v1, v2, v3, v4, v5, cen = p.verts
            verts[v_count+0] = tuple(v1)
            verts[v_count+1] = tuple(v2)
            verts[v_count+2] = tuple(v3)
            verts[v_count+3] = tuple(v4)
            verts[v_count+4] = tuple(v5)
            verts[v_count+5] = tuple(cen)
            color[v_count:v_count+6] = c

            index[i_count+0] = (v_count+5, v_count+0, v_count+1)
            index[i_count+1] = (v_count+5, v_count+1, v_count+2)
            index[i_count+2] = (v_count+5, v_count+2, v_count+3)
            index[i_count+3] = (v_count+5, v_count+3, v_count+4)
            index[i_count+4] = (v_count+5, v_count+4, v_count+0)

            lines[v_count+0] = (v_count+0, v_count+1)
            lines[v_count+1] = (v_count+1, v_count+2)
            lines[v_count+2] = (v_count+2, v_count+3)
            lines[v_count+3] = (v_count+3, v_count+4)
            lines[v_count+4] = (v_count+4, v_count+0)
            v_count += 6
            i_count += 5
        return verts, index, lines, color


def find_neighbors(face_set, face):
    return [f.verts[-1] for f in face_set if len(face.shared(f))==2]


def vert_to_faces(v, faces):
    return [f for f in faces if v in f.verts]
            


def trim(triplanet):
    # get every vert, find all edges, make new thing
    # do same for every face
    # use brute force ordering function
    new = HexPlanet()
    new.hexes = set()
    new.pents = set()
    done = set()
    for face in triplanet.faces:
        v1, v2, v3 = face.verts
        m12 = median(v1, v2, 2)
        m21 = median(v2, v1, 2)
        m23 = median(v2, v3, 2)
        m32 = median(v3, v2, 2)
        m31 = median(v3, v1, 2)
        m13 = median(v1, v3, 2)
        cn = (m12+m21+m23+m32+m31+m13)/6
        new.add_hex(m12, m21, m23, m32, m31, m13, cn)
        for v in face.verts:
            if v in done: continue
            adj_fs = vert_to_faces(v, triplanet.faces)
            adj_vs = set()
            for f in adj_fs:
                for p in f.verts:
                    adj_vs.add(p) if p not in adj_vs and p!=v else None
            assert len(adj_vs) == 5 or len(adj_vs) == 6, str(len(adj_vs))
            if len(adj_vs) == 5:
                v1, v2, v3, v4, v5 = arrange(adj_vs)
                m1 = median(v, v1, 2)
                m2 = median(v, v2, 2)
                m3 = median(v, v3, 2)
                m4 = median(v, v4, 2)
                m5 = median(v, v5, 2)
                cn = (m1+m2+m3+m4+m5)/5
                new.add_pen(m1, m2, m3, m4, m5, cn)
            elif len(adj_vs) == 6:
                v1, v2, v3, v4, v5, v6 = arrange(adj_vs)
                m1 = median(v, v1, 2)
                m2 = median(v, v2, 2)
                m3 = median(v, v3, 2)
                m4 = median(v, v4, 2)
                m5 = median(v, v5, 2)
                m6 = median(v, v6, 2)
                cn = (m1+m2+m3+m4+m5+m6)/6
                new.add_hex(m1, m2, m3, m4, m5, m6, cn)
            done.add(v)
    return new


class TriPlanet():
    def __init__(self, refine=0, force_refine=False):
        self.faces = set()
        self.adjacents = dict()

        t = ((1.0 + np.sqrt(5.0))) / 2.0
        verts = [
            (-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0),
            (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
            (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1),
        ]
        faces = [
            (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), # top
            (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8), # side a
            (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), # bottom
            (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1), # side b
        ]
        tags = [
            'refine', 'extrude', 'draw_faces', 'draw_lines', 'color'
        ]
        for i1, i2, i3 in faces:
            x1, y1, z1 = verts[i1]
            x2, y2, z2 = verts[i2]
            x3, y3, z3 = verts[i3]
            v1, v2, v3 = Vert(x1, y1, z1), Vert(x2, y2, z2), Vert(x3, y3, z3)
            v1, v2, v3 = v1.normalize(), v2.normalize(), v3.normalize()
            self.add(v1, v2, v3, tags)

        if refine > 3 and not force_refine:
            raise Warning
        for r in range(refine):
            self.refine(norm=True)

    def add(self, v1, v2, v3, tags=None):
        self.faces.add(Triangle(v1, v2, v3, tags=tags))
        for v in [v1, v2, v3]:
            if v not in self.adjacents:
                self.adjacents[v] = set()
        self.adjacents[v1] = self.adjacents[v1].union(set([v2, v3]))
        self.adjacents[v2] = self.adjacents[v2].union(set([v3, v1]))
        self.adjacents[v3] = self.adjacents[v3].union(set([v1, v2]))

    def get_faces(self, tags=None):
        return self.faces

    def refine(self, norm=True):
        old_faces = deepcopy(self.faces)
        self.faces = set()
        for face in old_faces:
            v1, v2, v3 = face.verts
            tags = ['refine', 'extrude', 'draw_lines', 'draw_faces', 'color']
            m1 = median(v1, v2)
            m2 = median(v2, v3)
            m3 = median(v3, v1)
            if norm:
                m1 = m1.normalize()
                m2 = m2.normalize()
                m3 = m3.normalize()
            self.add(v1, *near(v1, m1, m2, m3), tags=tags)
            self.add(v2, *near(v2, m1, m2, m3), tags=tags)
            self.add(v3, *near(v3, m1, m2, m3), tags=tags)
            self.add(m1, m2, m3, tags)

    def render(self):
        v_count = 0
        i_count = 0
        verts = np.zeros(shape=(len(self.faces)*3, 3), dtype=np.float32)
        index = np.zeros(shape=(len(self.faces), 3), dtype=np.uint32)
        lines = np.zeros(shape=(len(self.faces)*3, 2), dtype=np.uint32)
        color = np.zeros(shape=(len(self.faces)*3, 3), dtype=np.float32)
        for tri in self.faces:
            v1, v2, v3 = tri.verts
            i1, i2, i3 = v_count, v_count+1, v_count+2
            verts[i1, :] = tuple(v1)
            verts[i2, :] = tuple(v2)
            verts[i3, :] = tuple(v3)
            color[i1:i3+1, :] = np.random.random(size=(3))
            index[i_count] = (i1, i2, i3)
            if 'draw_lines' in tri.tags:
                lines[i1] = (i1, i2)
                lines[i2] = (i2, i3)
                lines[i3] = (i3, i1)
            v_count += 3
            i_count += 1
        return verts, index, lines, color


def extrude_hex(old, chance, da):
    new = HexPlanet()
    for h in old.hexes:
        v1, v2, v3, v4, v5, v6, vc = h.verts
        r = random.random()
        if r < chance:
            d1, d2, d3, d4, d5, d6, dc = v1*da, v2*da, v3*da, v4*da, v5*da, v6*da, vc*da
            new.add_hex(d1, d2, d3, d4, d5, d6, dc)

            new.add(v1, d1, v2)
            new.add(d2, d1, v2)
            new.add(v2, d2, v3)
            new.add(d3, d2, v3)
            new.add(v3, d3, v1)
            new.add(d1, d3, v1)
        else:
            new.add_hex(v1, v2, v3, v4, v5, v6, vc)
    #for face in old.sides:
        #new.add(*face, top=False)
    return new


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
    ico = TriPlanet()
    tags = ['refine', 'extrude', 'draw_faces', 'draw_lines', 'color']
    for i1, i2, i3 in faces:
        x1, y1, z1 = verts[i1]
        x2, y2, z2 = verts[i2]
        x3, y3, z3 = verts[i3]
        v1, v2, v3 = Vert(x1, y1, z1), Vert(x2, y2, z2), Vert(x3, y3, z3)
        v1, v2, v3 = normalize(v1), normalize(v2), normalize(v3)
        ico.add(v1, v2, v3, tags)
    return ico


def near(v, *args):
    d = {m:sum(distance(v, m)) for m in args}
    l = sorted(d.items(), key=lambda x: x[1])
    return l[0][0], l[1][0]


def nearest(v1, verts, n=1):
    distances = {v2:sum(distance(v1, v2)) for v2 in verts}
    ordered_dis = sorted(distances.items(), key=lambda x: x[1])
    ordered_ver = [v2 for v2, d in ordered_dis]
    return ordered_ver[0:n+1]


def arrange(verts):
    if len(verts) <= 1:
        return [verts[0]]
    verts = list(verts)
    head, tail = verts[0], verts[1:]
    order = [head]
    while len(tail) > 1:
        head = nearest(head, tail)[0]
        order.append(head)
        tail.remove(head)
    order.append(tail[0])
    return order


def distance(v1, v2):
    return abs(v1-v2)


def median(v1, v2, weight=1):
    return ((v1*weight)+v2)/(weight+1)


def center(v1, v2, v3):
    return (v1+v2+v3)/3
