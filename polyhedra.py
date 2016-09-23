
import math
import uuid
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
        self.handle = uuid.uuid4()
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


# maybe we should just keep the actual nodes in these
# we aren't preventing dupilcates because of the color problems
# so there isn't much point adding the extra level of indirection.
class PolyFace:
    def __init__(self, cent_node, prev_node, next_node, group=0, original=None):
        self.handle = uuid.uuid4()
        self.touch = None
        self.group = group
        self.cent_node = cent_node
        self.prev_node = prev_node
        self.next_node = next_node
        self.a = None
        self.b = None
        self.c = None
        self.original = original

    def n_shared_nodes(self, other_face, node_lookup):
        pass

    def halve(self):
        # new points halfway between each pair of vertices
        # return four faces
        # one gets one old connection, two new ones
        # the center gets all new connections
        pass

    def thirds(self):
        pass


def tesselate(poly):
    # try to do it in place, maintaining connections
    n = deepcopy(poly.nodes)
    f = deepcopy(poly.faces)
    for h_face in f:
        # how about instead of adding new nodes
        # we take existing nodes and split them
        face = f[h_face]
        m_oppo = (n[face.next_node] + n[face.prev_node])/2
        m_prev = (n[face.cent_node] + n[face.prev_node])/2
        m_next = (n[face.cent_node] + n[face.next_node])/2
        h_oppo = poly.add_node(*tuple(m_oppo))
        h_prev = poly.add_node(*tuple(m_prev))
        h_next = poly.add_node(*tuple(m_next))
        poly.add_face(face.cent_node, h_prev, h_next)
        poly.add_face(h_prev, face.prev_node, h_oppo)
        poly.add_face(h_oppo, face.next_node, h_next)
        poly.add_face(h_oppo, h_prev, h_next)
        del poly.faces[h_face]


# new algo:
# get copies of old faces and nodes
# do two loops, one for faces and one for nodes
# for each face, take thirds, preserving objects, etc
# for each node, move a third down each connection (which we'll have to track)
# and make a face like that.
# should be over in O(n)
def hexify(poly):
    n = deepcopy(poly.nodes)
    f = deepcopy(poly.faces)
    for h_face in f:
        face = f[h_face]
        del poly.faces[h_face]

        # midpoints, each a third across one edge of the triangle
        m_oppo_l = (n[face.next_node] + n[face.prev_node]*2)/3
        m_oppo_r = (n[face.next_node]*2 + n[face.prev_node])/3
        m_prev_n = (n[face.cent_node]*2 + n[face.prev_node])/3
        m_prev_f = (n[face.cent_node] + n[face.prev_node]*2)/3
        m_next_n = (n[face.cent_node]*2 + n[face.next_node])/3
        m_next_f = (n[face.cent_node] + n[face.next_node]*2)/3
        m_center = sum([m_oppo_l, m_oppo_r, m_prev_n, m_prev_f, m_next_n, m_next_f])/6

        # new node handles
        # all part of same group
        group_id = uuid.uuid4()
        h_oppo_l = poly.add_node(*tuple(m_oppo_l), group=group_id)
        h_oppo_r = poly.add_node(*tuple(m_oppo_r), group=group_id)
        h_prev_n = poly.add_node(*tuple(m_prev_n), group=group_id)
        h_prev_f = poly.add_node(*tuple(m_prev_f), group=group_id)
        h_next_n = poly.add_node(*tuple(m_next_n), group=group_id)
        h_next_f = poly.add_node(*tuple(m_next_f), group=group_id)
        h_center = poly.add_node(*tuple(m_center), group=group_id)
        # consistent color
        # NOTE: must have duplicate vertices for each face
        # for the colors to lay flat and not blend.
        poly.colors[group_id] = np.random.random(3)

        # size faces of hexagon
        poly.add_face(h_center, h_oppo_l, h_oppo_r, group=group_id)
        poly.add_face(h_center, h_oppo_r, h_next_f, group=group_id)
        poly.add_face(h_center, h_next_f, h_next_n, group=group_id)
        poly.add_face(h_center, h_next_n, h_prev_n, group=group_id)
        poly.add_face(h_center, h_prev_n, h_prev_f, group=group_id)
        poly.add_face(h_center, h_prev_f, h_oppo_l, group=group_id)

        m_old_cent = n[face.cent_node]
        m_old_prev = n[face.prev_node]
        m_old_next = n[face.next_node]
        # center triangle/part of hex
        #extra_id = uuid.uuid4()
        extra_id = 1000000 # for later testing
        # part of pentagon? only get one tri at a time
        h_old_cent = poly.add_node(*tuple(m_old_cent), group=extra_id)
        h_old_prev = poly.add_node(*tuple(m_old_prev), group=extra_id)
        h_old_next = poly.add_node(*tuple(m_old_next), group=extra_id)
        # copies of new nodes
        c_oppo_l = poly.add_node(*tuple(m_oppo_l), group=extra_id)
        c_oppo_r = poly.add_node(*tuple(m_oppo_r), group=extra_id)
        c_prev_n = poly.add_node(*tuple(m_prev_n), group=extra_id)
        c_prev_f = poly.add_node(*tuple(m_prev_f), group=extra_id)
        c_next_n = poly.add_node(*tuple(m_next_n), group=extra_id)
        c_next_f = poly.add_node(*tuple(m_next_f), group=extra_id)
        # just set all to one color?
        poly.colors[extra_id] = np.array([0.0, 0.0, 0.0])
        poly.add_face(h_old_cent, c_next_n, c_prev_n, group=extra_id)
        poly.add_face(h_old_prev, c_prev_f, c_oppo_l, group=extra_id)
        poly.add_face(h_old_next, c_next_f, c_oppo_r, group=extra_id)


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
    for n in poly.nodes.values():
        n.normalize()


class Polyhedron:
    # real requirement:
    # for every face, we need to have ordered edges
    # and easy access to neighboring faces
    # and we have to maintain that for every iteration
    def __init__(self):
        self.nodes = {}
        self.faces = {}
        self.sides = {}
        self.colors = {}

    def add_node(self, x, y, z, group=0, normalize=False):
        node = PolyNode(x, y, z, group=group)
        if normalize: node.normalize()
        #for h, n in self.nodes.items():  #disable duplicate check for color interp.
            #if node == n:
                #return h
        self.nodes[node.handle] = node
        return node.handle

    def add_face(self, hc, hl, hr, group=0):  # TODO: check for dupes
        face = PolyFace(hc, hl, hr, group=group)
        self.faces[face.handle] = face
        return face.handle

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
            for i, n in enumerate([face.cent_node, face.next_node, face.prev_node]):
                node = self.nodes[n]
                rand_color = np.random.random(3)
                if node.group != 0 and node.group in self.colors.keys():
                    color[count+i] = self.colors[node.group]
                else:
                    color[count:count+3] = rand_color
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
            hc = self.add_node(*v[i1])
            hl = self.add_node(*v[i2])
            hr = self.add_node(*v[i3])
            face = self.add_face(hc, hl, hr)


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
