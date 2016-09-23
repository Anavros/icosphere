
import math
from uuid import uuid4 as uuid
import numpy as np
import random
import itertools
from copy import deepcopy


# new idea
# base it around iterating over points at effectively random
# each point stores how many faces are connected to it
# and each face knows it's orientation
# we can check if the face center is at the point
# otherwise we can check the other points on the face
# one of them will match
# extrapolate the rest from there
# this gives access to each face and each vertex


class PolyNode:
    def __init__(self, x, y, z, group=0):
        self.handle = uuid()
        self.touch = None
        self.group = group
        self.x = x
        self.y = y
        self.z = z

    def _cast(self, x):
        return x if type(x) is PolyNode else PolyNode(x, x, x)

    def __iter__(self):
        for a in [self.x, self.y, self.z]: yield a

    def __eq__(self, vert): # BUG prone to floating-point errors!
        return self.x==vert.x and self.y==vert.y and self.z==vert.z

    def __repr__(self):
        return "Node({:.2f}, {:.2f}, {:.2f})".format(self.x, self.y, self.z)

    def __add__(self, x):
        v = self._cast(x)
        return PolyNode(self.x+v.x, self.y+v.y, self.z+v.z)

    def __radd__(self, x): # for sum()
        return self.__add__(x)

    def __mul__(self, x):
        v = self._cast(x)
        return PolyNode(self.x*v.x, self.y*v.y, self.z*v.z)

    def __truediv__(self, x):
        v = self._cast(x)
        return PolyNode(self.x/v.x, self.y/v.y, self.z/v.z)

    def extend(self, n):
        """Transform the node's length with respect to the center of the shape."""
        self.move(self.x*n, self.y*n, self.z*n)

    def normalize(self):
        l = math.sqrt(sum(self*self))
        self.move(self.x/l, self.y/l, self.z/l)

    def move(self, x, y, z):
        """Move node to a new point in space while maintaining its connections."""
        self.x = x
        self.y = y
        self.z = z


class PolyFace:
    def __init__(self, a, b, c, group=0):
        self.handle = uuid()
        self.touch = None
        self.group = group
        self.a = a
        self.b = b
        self.c = c

    def __iter__(self):
        for node in [self.a, self.b, self.c]:
            yield node

    def normalize(self):
        for node in self:
            node.normalize()

    def halves(self):
        ab = (self.a + self.b)/2
        bc = (self.b + self.c)/2
        ca = (self.c + self.a)/2
        return ab, bc, ca

    def thirds(self):
        aab = (self.a*2 + self.b)/3
        abb = (self.a + self.b*2)/3
        bbc = (self.b*2 + self.c)/3
        bcc = (self.b + self.c*2)/3
        cca = (self.c*2 + self.a)/3
        caa = (self.c + self.a*2)/3
        center = sum([aab, abb, bbc, bcc, cca, caa])/6
        return aab, abb, bbc, bcc, cca, caa, center


def tesselate(poly):
    # TODO: deepcopies are expensive
    new_faces = {}  # TODO: insert directly here instead of using add_face
    for face in deepcopy(poly.faces).values():  # can't have it changing while iterating
        ab, bc, ca = face.halves()
        #poly.add_node(*tuple(ab))  # TODO edit add* funcs to take tuples directly
        #poly.add_node(*tuple(bc))
        #poly.add_node(*tuple(ca))
        poly.add_face(face.a, ab, ca)
        poly.add_face(face.b, ab, bc)
        poly.add_face(face.c, bc, ca)
        poly.add_face(ab, bc, ca)
        del poly.faces[face.handle]


# new algo:
# get copies of old faces and nodes
# do two loops, one for faces and one for nodes
# for each face, take thirds, preserving objects, etc
# for each node, move a third down each connection (which we'll have to track)
# and make a face like that.
# should be over in O(n)
def hexify(poly):
    f = deepcopy(poly.faces)
    for face in f.values():
        aab, abb, bbc, bcc, cca, caa, center = face.thirds()

        # six faces of hexagon
        group_id = uuid()
        poly.add_face(center, aab, abb, group=group_id)
        poly.add_face(center, abb, bbc, group=group_id)
        poly.add_face(center, bbc, bcc, group=group_id)
        poly.add_face(center, bcc, cca, group=group_id)
        poly.add_face(center, cca, caa, group=group_id)
        poly.add_face(center, caa, aab, group=group_id)
        poly.colors[group_id] = np.random.random(3)

        # extra face; part of hex/pent
        extra_id = 1 # for later testing
        poly.add_face(face.a, aab, caa, group=extra_id)
        poly.add_face(face.b, bbc, abb, group=extra_id)
        poly.add_face(face.c, cca, bcc, group=extra_id)
        poly.colors[extra_id] = np.array([0.0, 0.0, 0.0])

        del poly.faces[face.handle]


def extrude(poly):
    # each group id gets a new elevation
    # for sides:
    # when you extrude a node, leave the old node behind and connect them
    # although I don't know what to do about diagonals
    # that might not work until we get some more ordered structure
    lengths = {}
    for node in poly.nodes.values():
        try:
            l = lengths[node.group]
        except KeyError:
            l = random.choice([0.9, 1.0, 1.1])
            lengths[node.group] = l
        finally:
            node.extend(l)
    #return poly  # mutates, no return


def normalize(poly):
    for f in poly.faces.values():
        f.normalize()


class Polyhedron:
    def __init__(self):
        self.nodes = {}
        self.faces = {}
        self.sides = {}
        self.colors = {}

    def add_node(self, x, y, z, group=0):
        # TODO: keep track of connected nodes
        # or not?
        node = PolyNode(x, y, z, group=group)
        self.nodes[node.handle] = node
        return node

    def add_face(self, a, b, c, group=0):
        face = PolyFace(a, b, c, group=group)
        self.faces[face.handle] = face
        return face

    def construct_buffers(self):
        count = 0
        verts = np.zeros(shape=(len(self.faces)*3, 3), dtype=np.float32)
        color = np.zeros(shape=(len(self.faces)*3, 3), dtype=np.float32)
        index = np.zeros(shape=(len(self.faces)*3),    dtype=np.uint32)
        lines = np.zeros(shape=(len(self.faces)*3, 2), dtype=np.uint32)
        for face in self.faces.values():
            verts[count+0, :] = tuple(face.a)  # TODO: move inside loop
            verts[count+1, :] = tuple(face.b)
            verts[count+2, :] = tuple(face.c)
            if face.group in self.colors.keys():
                color[count:count+3] = self.colors[face.group]
            else:
                color[count:count+3] = np.random.random(3)
            #else:
                #color[count:count+3] = np.random.random(3)
            index[count+0] = count+0
            index[count+1] = count+1  # messy, fix later
            index[count+2] = count+2
            count += 3
        return verts, index, lines, color


class Icosahedron(Polyhedron):
    def __init__(self):
        Polyhedron.__init__(self)

        t = ((1.0 + np.sqrt(5.0))) / 2.0
        v = [
            (-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0),
            (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
            (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1),
        ]
        f = [
            (0, 11,  5),    # next
            (0,  5,  1),    # next
            (0,  1,  7),    # next
            (0,  7,  10),   # next
            (0, 10, 11),    # flip

            (2, 11, 10),    # side-next

            (4,  5, 11),    # side-next
            (9,  1,  5),    # side-next
            (8,  7,  1),    # side-next
            (6, 10,  7),    # side-next

            (4,  9,  5),    # side-next
            (9,  8,  1),    # side-next
            (8,  6,  7),    # side-next
            (6,  2, 10),    # flip
            (2,  4, 11),    # side-next?

            (3,  9,  4),    # next
            (3,  4,  2),    # next
            (3,  2,  6),    # next
            (3,  6,  8),    # next
            (3,  8,  9),    # end

            #(4, 5, 11), (9, 1, 5), (8, 7, 1), (6, 10, 7), (2, 11, 10),
            #(5, 4, 9), (11, 2, 4), (10, 6, 2), (7, 6, 8), (1, 9, 8),
        ]
        for i1, i2, i3 in f:
            a = self.add_node(*v[i1])
            b = self.add_node(*v[i2])
            c = self.add_node(*v[i3])
            face = self.add_face(a, b, c)


class FlatTile(Polyhedron):
    def __init__(self):
        Polyhedron.__init__(self)
        v = [
            (0.0, 0.0, 0.0),    # 0, center
            (-0.50, +1.0, 0.0), # 1, top-left
            (+0.50, +1.0, 0.0), # 2, top-right
            (+1.0,   0.0, 0.0), # 3, right
            (+0.50, -1.0, 0.0), # 4, bottom-right
            (-0.50, -1.0, 0.0), # 5, bottom-left
            (-1.0,   0.0, 0.0), # 6, left
        ]
        f = [
            (0, 1, 2), # north
            (0, 2, 3), # north-east
            (0, 3, 4), # south-east
            (0, 4, 5), # south
            (0, 5, 6), # south-west
            (0, 6, 1), # north-west
        ]

        for i1, i2, i3 in f:
            hc = self.add_node(*v[i1])
            hl = self.add_node(*v[i2])
            hr = self.add_node(*v[i3])
            face = self.add_face(hc, hl, hr)
