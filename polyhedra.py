
import math
import uuid
import numpy as np
import itertools


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
    def __init__(self, x, y, z):
        self.handle = uuid.uuid4()
        self.touch = None
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

    def normalize(self):
        l = math.sqrt(sum(self*self))
        self.move(self.x/l, self.y/l, self.z/l)

    def move(self, x, y, z):
        """Move node to a new point in space while maintaining its connections."""
        self.x = x
        self.y = y
        self.z = z


class PolyFace:
    def __init__(self, cent_node, prev_node, next_node, original=None):
        PolyAttr.__init__(self)
        self.cent_node = cent_node
        self.prev_node = prev_node
        self.next_node = next_node
        self.original = original

        # do the point hex for the left point if we're moving right
        # actually check to do the center and the left
        # for the center:
        # place left near point in list
        # move right, place that left point
        # continue until the rightmost triangle is the original
        # points are now in ordered list
        # add new shape

def tesselate(old):
    new = Polyhedron()
    n = old.nodes
    f = old.faces
    for node in n.values():
        near_points = []
        for h in node.clockwise():
            # TODO: add flags to prevent doing the same spot twice
            face = old.faces[h]
            mln, mlf = thirds(face.hc, face.hl)
            mrn, mrf = thirds(face.hc, face.hr)
            mol, mor = thirds(face.hl, face.hl)
            cn = center(mln, mlf, mrn, mrf, mol, mor)
            new.add_node(mln)
            new.add_node(mlf)
            new.add_node(mrn)
            new.add_node(mrf)
            new.add_node(mol)
            new.add_node(mor)
            new.add_node(cn)

            # solves the mid-face hexes, 6/13
            f1 = new.add_face(cn, mln, mlf)
            f2 = new.add_face(cn, mlf, mol)
            f3 = new.add_face(cn, mol, mor)
            f4 = new.add_face(cn, mor, mrf)
            f5 = new.add_face(cn, mrf, mrn)
            f6 = new.add_face(cn, mrn, mln)
            near_points.append(mln)

            cn.faces = [f1, f2, f3, f4, f5, f6]
            mln.faces = 

        # solves the center hex (and pents), 7/13
        if len(near_points) == 5:
            pass
            #new.add_face(*near_points)
        # so what about the connectivity?
        # actually, each of those points will get its own pass anyway
        # so we might only need 7
    return new


class Polyhedron:
    # real requirement:
    # for every face, we need to have ordered edges
    # and easy access to neighboring faces
    # and we have to maintain that for every iteration
    def __init__(self):
        self.nodes = {}
        self.faces = {}

    def add_node(self, x, y, z):
        node = PolyNode(x, y, z)
        for h, n in self.nodes.items():
            if node == n:
                return h
        self.nodes[node.handle] = node

    def add_face(self, nc, nl, nr):  # TODO: check for dupes
        face = PolyFace(hc, hl, hr)
        self.faces[face.handle] = face

    def shared(self, a, b):
        return self.nodes[a] == self.nodes[b]

    def touched(self, handle):
        return self.touch == self.faces[handle].touch

    def construct_buffers(self):
        count = 0
        verts = np.zeros(shape=(len(self.faces)*3, 3), dtype=np.float32)
        color = np.zeros(shape=(len(self.faces)*3, 3), dtype=np.float32)
        index = np.zeros(shape=(len(self.faces)*3),    dtype=np.uint32)
        lines = np.zeros(shape=(len(self.faces)*3, 2), dtype=np.uint32)
        for face in self.faces.values():
            verts[count+0, :] = tuple(self.nodes[face.cent_node])
            verts[count+1, :] = tuple(self.nodes[face.next_node])
            verts[count+2, :] = tuple(self.nodes[face.prev_node])
            color[count:count+3] = np.random.random(3)
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
            vc = PolyNode(*v[i1]) # TODO fix redundancy by checking for existance
            vl = PolyNode(*v[i2])
            vr = PolyNode(*v[i3])
            self.nodes[vc.handle] = vc
            self.nodes[vl.handle] = vl
            self.nodes[vr.handle] = vr
            new = PolyFace(vc.handle, vl.handle, vr.handle, original=(i1, i2, i3))
            self.faces[new.handle] = new
            if not self.point: self.point = new.handle
            if not self.touch: self.touch = uuid.uuid4()
        self.autoconnect()


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
