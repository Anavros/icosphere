
import numpy as np
from math import sqrt
from random import choice
from uuid import uuid4 as uuid


class PolyNode:
    def __init__(self, coords, group=0):
        x, y, z = coords
        self.group = group
        self.touch = 0
        self.x = x
        self.y = y
        self.z = z

    def _cast(self, x):
        return x if type(x) is PolyNode else PolyNode((x, x, x))

    def __iter__(self):
        for a in [self.x, self.y, self.z]: yield a

    def __eq__(self, vert): # BUG prone to floating-point errors!
        return self.x==vert.x and self.y==vert.y and self.z==vert.z

    def __repr__(self):
        return "Node({:.2f}, {:.2f}, {:.2f})".format(self.x, self.y, self.z)

    def __add__(self, x):
        v = self._cast(x)
        return PolyNode((self.x+v.x, self.y+v.y, self.z+v.z))

    def __radd__(self, x): # for sum()
        return self.__add__(x)

    def __mul__(self, x):
        v = self._cast(x)
        return PolyNode((self.x*v.x, self.y*v.y, self.z*v.z))

    def __truediv__(self, x):
        v = self._cast(x)
        return PolyNode((self.x/v.x, self.y/v.y, self.z/v.z))

    def extrude(self, n):
        """Transform the node's length with respect to the center of the shape."""
        self.move(self.x*n, self.y*n, self.z*n)

    def normalize(self, n=1):
        length = sqrt(sum(self*self))
        self.move(self.x/(length/n), self.y/(length/n), self.z/(length/n))

    def move(self, x, y, z):
        """Move node to a new point in space while maintaining its connections."""
        self.x = x
        self.y = y
        self.z = z


class PolyFace:
    def __init__(self, nodes, group=0):
        a, b, c = nodes
        self.group = group
        self.a = PolyNode(a)  # force duplicates
        self.b = PolyNode(b)
        self.c = PolyNode(c)

    def __iter__(self):
        for node in [self.a, self.b, self.c]:
            yield node

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


class PolyGroup:
    def __init__(self, faces, group_id):
        self.faces = faces
        self.group = group_id

    def __iter__(self):
        for face in self.faces:
            yield face


class Polyhedron:
    def __init__(self):
        self.faces = []
        #self.sides = {}
        self.colors = {}

    def tesselate(poly):
        new_faces = []
        for face in poly.faces:
            ab, bc, ca = face.halves()
            new_faces.append(PolyFace((face.a, ab, ca), group=uuid()))
            new_faces.append(PolyFace((face.b, ab, bc), group=uuid()))
            new_faces.append(PolyFace((face.c, bc, ca), group=uuid()))
            new_faces.append(PolyFace((ab, bc, ca), group=uuid()))
        poly.faces = new_faces

    def hexify(poly):
        new_faces = []
        extra_group_centers = {}  # center node -> group id
        extra_groups = {}  # group id -> list of faces
        for face in poly.faces:
            aab, abb, bbc, bcc, cca, caa, center = face.thirds()

            # six faces of hexagon
            group_id = uuid()
            new_faces.append(PolyFace((center, aab, abb), group=group_id))
            new_faces.append(PolyFace((center, abb, bbc), group=group_id))
            new_faces.append(PolyFace((center, bbc, bcc), group=group_id))
            new_faces.append(PolyFace((center, bcc, cca), group=group_id))
            new_faces.append(PolyFace((center, cca, caa), group=group_id))
            new_faces.append(PolyFace((center, caa, aab), group=group_id))
            poly.colors[group_id] = np.random.random(3)

            # extra face; part of hex/pent
            #extra_id = 1 # for later testing
            #new_faces.append(PolyFace((face.a, aab, caa), group=extra_id))
            #new_faces.append(PolyFace((face.b, bbc, abb), group=extra_id))
            #new_faces.append(PolyFace((face.c, cca, bcc), group=extra_id))
            #poly.colors[extra_id] = np.array([0.0, 0.0, 0.0])

            # new extra face:
            #new_faces.append(PolyFace((face.a, aab, caa), group=extra_id))
            # first, see if a group already exists
            # it will be grouped around its center point, face.a
            # so lookup if face.a has already been started
            # if not, start a new group with face.a
            # if so, add it to that group
            extra_sets = [
                (face.a, aab, caa),
                (face.b, bbc, abb),
                (face.c, cca, bcc),
            ]
            for new_center, a, b in extra_sets:
                try:
                    extra_id = extra_group_centers[ tuple(new_center) ]  # highlight error
                except KeyError:
                    extra_id = uuid()
                    poly.colors[extra_id] = np.random.random(3)
                    extra_group_centers[ tuple(new_center) ] = extra_id

                face = PolyFace((new_center, a, b), group=extra_id)
                try:
                    extra_groups[extra_id].append(face)
                except KeyError:
                    extra_groups[extra_id] = [face]
                new_faces.append(face)

        poly.faces = new_faces

    def extrude(poly):
        lengths = {}
        for face in poly.faces:
            try:
                l = lengths[face.group]
            except KeyError:
                l = choice([0.95, 1.0, 1.05])
                lengths[face.group] = l
            finally:
                for node in face:
                    node.extrude(l)

    def normalize(poly):
        for f in poly.faces:
            for n in f:
                n.normalize()

    def construct_buffers(self):
        count = 0
        verts = np.zeros(shape=(len(self.faces)*3, 3), dtype=np.float32)
        color = np.zeros(shape=(len(self.faces)*3, 3), dtype=np.float32)
        index = np.zeros(shape=(len(self.faces)*3),    dtype=np.uint32)
        lines = np.zeros(shape=(len(self.faces)*3, 2), dtype=np.uint32)
        for face in self.faces:
            for i, node in enumerate(face):
                verts[count+i, :] = tuple(node)
                index[count+i] = count+i
            try:
                face_color = self.colors[face.group]
            except KeyError:
                face_color = np.random.random(3)
            color[count:count+3] = face_color  # set all three nodes to same color
            count += 3
        return verts, index, lines, color

    def construct_side_buffers(self):
        count = 1
        verts = np.zeros(shape=(len(self.faces)*3 + 1, 3), dtype=np.float32)
        #color = np.zeros(shape=(len(self.faces)*3 + 1, 3), dtype=np.float32)
        index = np.zeros(shape=(len(self.faces)*3 + 1, 3), dtype=np.uint32)
        verts[0, :] = [0, 0, 0]  # origin point
        #color[0, :] = [0, 0, 0]
        for a, b, c in self.faces:
            verts[count+0] = tuple(a)
            verts[count+1] = tuple(b)
            verts[count+2] = tuple(c)
            index[count+0] = [0, count+0, count+1]
            index[count+1] = [0, count+1, count+2]
            index[count+2] = [0, count+2, count+0]
            count += 3
        return verts, index

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
            a = PolyNode(v[i1])
            b = PolyNode(v[i2])
            c = PolyNode(v[i3])
            self.faces.append(PolyFace((a, b, c), group=uuid()))


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
            a = PolyNode(v[i1])
            b = PolyNode(v[i2])
            c = PolyNode(v[i3])
            self.faces.append(PolyFace((a, b, c), group=uuid()))
