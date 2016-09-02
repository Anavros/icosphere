
import math
import uuid
import numpy as np


class PolyAttr:
    # contains hash id?
    def __init__(self):
        self.handle = uuid.uuid4()
        self.touch = 0
        self.tags = []


class PolyNode(PolyAttr):
    # contains incoming and outgoing edges?
    def __init__(self, x, y, z):
        PolyAttr.__init__(self)
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        for a in [self.x, self.y, self.z]:
            yield a

    def move(self, x, y, z):
        """Move node to a new point in space while maintaining its connections."""


class PolyEdge(PolyAttr):
    def __init__(self):
        PolyAttr.__init__(self)


class PolyFace(PolyAttr):
    def __init__(self, cent_node, prev_node, next_node):
        PolyAttr.__init__(self)
        # only holds the ids for table lookups?
        self.cent_node = cent_node
        self.prev_node = prev_node
        self.next_node = next_node
        self.flip_face = 0
        self.prev_face = 0
        self.next_face = 0

        # do the point hex for the left point if we're moving right
        # actually check to do the center and the left
        # for the center:
        # place left near point in list
        # move right, place that left point
        # continue until the rightmost triangle is the original
        # points are now in ordered list
        # add new shape


class Polyhedron:
    def __init__(self):
        self.nodes = {}
        self.faces = {}

    def shared(self, a, b):
        return self.nodes[a] == self.nodes[b]

    def construct_buffers(self):
        # we can assume each face is a triangle
        # as nothing else is allowed
        # hexes and pentagons are accessed by traversing
        # and counting the number of triangles surrounding a center point
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
            #lines[count+0] = tuple(self.nodes[face.cent_node]),\
                #tuple(self.nodes[face.next_node])
            #lines[count+1] = tuple(self.nodes[face.next_node]),\
                #tuple(self.nodes[face.prev_node])
            #lines[count+2] = tuple(self.nodes[face.prev_node]),\
                #tuple(self.nodes[face.cent_node])
            count += 3
        return verts, index, lines, color


class Icosahedron(Polyhedron):
    def __init__(self):
        Polyhedron.__init__(self)

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


class FlatTile(Polyhedron):
    def __init__(self):
        Polyhedron.__init__(self)
        v = [
            (0.0, 0.0, 0.0),    # 0, center
            (-0.75, +1.0, 0.0), # 1, top-left
            (+0.75, +1.0, 0.0), # 2, top-right
            (+1.0,   0.0, 0.0), # 3, right
            (+0.75, -1.0, 0.0), # 4, bottom-right
            (-0.75, -1.0, 0.0), # 5, bottom-left
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

        #first = TriFace(v[0], v[1], v[2])
        #first.vc = v[0]
        #first.vl = v[1]
        #first.vr = v[2]

        #force_search()
        #new = TriFace(v[0], v[2], v[3])  # north east, should be first.rotate
        # matches v[0], v[2]
        # first.v1 = this.v1, first.v2 = no match, first.v3 = this.v2
        # because the centers are the same, it's not a flip
        # the left coord is not included, so it isn't reverse
        # the first.vr IS included, so this must be first's rotate

        # logic:
        # last.vc == this.vc? not flip
        # last.vl == this.vl? could that even happen?
        # last.vl == this.vr? last.rotate = this, this.reverse = last
        # last.vr == this.vl? last.reverse = this, this.rotate = last
        # last.vc != this.vc, last.vr == this.vl, last.vl == this.vr? both flips
        for i1, i2, i3 in f:
            vc = PolyNode(*v[i1])
            vl = PolyNode(*v[i2])
            vr = PolyNode(*v[i3])
            self.nodes[vc.handle] = vc
            self.nodes[vl.handle] = vl
            self.nodes[vr.handle] = vr
            new = PolyFace(vc.handle, vl.handle, vr.handle)
            for old in self.faces.values(): # O(n) slow but simple
                if self.shared(old.cent_node, new.cent_node) \
                    and self.shared(old.prev_node, new.next_node):
                    old.prev_face = new.handle
                    new.next_face = old.handle
                elif self.shared(old.cent_node, new.cent_node) \
                    and self.shared(old.next_node, new.prev_node):
                    old.next_face = new.handle
                    new.prev_face = old.handle
                elif not self.shared(old.cent_node, new.cent_node) \
                    and self.shared(old.prev_node, new.next_node) \
                    and self.shared(old.next_node, new.prev_node):
                    old.flip_face = new.handle
                    new.flip_face = old.handle
            self.faces[new.handle] = new
