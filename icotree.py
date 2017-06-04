
import numpy as np
from math import sqrt
from copy import deepcopy


# Identification Scheme:
# 1, 1-A, 1-A-A, 1-A-A-A
# 1.a, 1-A.a, 1-A-A.down_a
# 1.down_a == 1_A


# Some conventions used in this file:
# Points are triplets of floats, like (1.5, 0.5, -0.5).
# Names like a, b, and c are points.
# Triangles are triplets of points.
# Names like v1, v2, v3 are triangles.
# All hexagons are flat-topped.

# What the various points mean for each hexagon.
# I'd like a more detailed graph that shows face names and links too.
# But that would take up a lot of space.
#      f---------a
#     / \down_a / \
#    /   \     /   \
#   /     \   /     \
#  /down_f \ /down_b \
# e---------m---------b
#  \down_e / \down_c /
#   \     /   \     /
#    \   /     \   /
#     \ /down_d \ /
#      d---------c


def test():
    # The golden mean, phi, used in construction of the initial icosahedron.
    t = (1.0 + sqrt(5.0)) / 2.0
    # The vertices of the icosahedron.
    v = [
        (-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0),
        (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
        (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1),
    ]
    # The faces, as triplet indices into the previous list, representing triangles.
    f = [
        (0, 11,  5), (0,  5,  1), (0,  1,  7), (0,  7, 10), (0, 10, 11),
        (2, 11, 10), (4,  5, 11), (9,  1,  5), (8,  7,  1), (6, 10,  7),
        (4,  9,  5), (9,  8,  1), (8,  6,  7), (6,  2, 10), (2,  4, 11),
        (3,  9,  4), (3,  4,  2), (3,  2,  6), (3,  6,  8), (3,  8,  9),
    ]
    points = {
         0: (11,  5,  1,  7, 10),
         1: ( 5,  0,  7,  8,  9),
         2: (11, 10,  6,  3,  4),
         3: ( 9,  4,  2,  6,  8),
         4: ( 5, 11,  9,  2,  3),
         5: ( 0, 11,  1,  4,  9),
         6: ( 8,  7,  2, 10,  3),
         7: ( 0,  1, 10,  8,  6),
         8: ( 7,  1,  9,  6,  3),
         9: ( 4,  5,  1,  8,  3),
        10: ( 0,  7, 11,  2,  6),
        11: ( 0,  5, 10,  2,  4),
    }
    for i1, i2, i3 in f:
        v1 = v[i1]
        v2 = v[i2]
        v3 = v[i3]
        a, b, c, d, e, f, m = hexpoints(v1, v2, v3)
    for point, indices in points.items():
        i1, i2, i3, i4, i5 = indices  # this needs to be ordered manually
        v1 = v[i1]
        v2 = v[i2]
        v3 = v[i3]
        v4 = v[i4]
        v5 = v[i5]
        a, _ = thirds(point, v1)
        b, _ = thirds(point, v2)
        c, _ = thirds(point, v3)
        d, _ = thirds(point, v4)
        e, _ = thirds(point, v5)
    

class Icosphere:
    def __init__(s, depth):
        # This is where faces are stored.
        # Their keys are strings that represent their position within the graph.
        # This indirect method is used for lazy evaluation, essentially.
        # When a face subdivides, it tries to link its divisions to the divisions
        # of its neighbors. However, its neighbors haven't been divided yet, so
        # those faces don't exist at that time. When string symbols are used, faces
        # can be linked together before their positions are set.
        #s.faces = {}
        # Come to think of it, there might be a better way to do this.
        # If we did two passes, one to place the points, and another to link the graph.
        s.faces = []
        s.depth = depth

        # The golden mean, phi, used in construction of the initial icosahedron.
        t = (1.0 + sqrt(5.0)) / 2.0
        # The vertices of the icosahedron.
        v = [
            (-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0),
            (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
            (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1),
        ]
        # The faces, as triplet indices into the previous list, representing triangles.
        f = [
            (0, 11,  5), (0,  5,  1), (0,  1,  7), (0,  7, 10), (0, 10, 11),
            (2, 11, 10), (4,  5, 11), (9,  1,  5), (8,  7,  1), (6, 10,  7),
            (4,  9,  5), (9,  8,  1), (8,  6,  7), (6,  2, 10), (2,  4, 11),
            (3,  9,  4), (3,  4,  2), (3,  2,  6), (3,  6,  8), (3,  8,  9),
        ]
        points = {
             0: ( 1,  5, 11, 10,  7),
             1: ( 8,  9,  5,  0,  7),
             2: (11,  4,  3,  6, 10),
             3: ( 4,  2,  6,  8,  9),
             4: ( 3,  9,  5, 11,  2),
             5: ( 0,  1,  9,  4, 11),
             6: ( 7,  8,  3,  2, 10),
             7: ( 0,  1,  8,  6, 10),
             8: ( 1,  9,  3,  6,  7),
             9: ( 3,  4,  5,  1,  8),
            10: ( 6,  7,  0, 11,  2),
            11: ( 0,  5,  4,  2, 10),
        }

        for i1, i2, i3 in f:
            v1 = v[i1]
            v2 = v[i2]
            v3 = v[i3]
            s.faces.append(Face(*hexpoints(v1, v2, v3)))

        for point, indices in points.items():
            i1, i2, i3, i4, i5 = indices  # this needs to be ordered manually
            vm = v[point]
            v1 = v[i1]
            v2 = v[i2]
            v3 = v[i3]
            v4 = v[i4]
            v5 = v[i5]
            a, _ = thirds(vm, v1)
            b, _ = thirds(vm, v2)
            c, _ = thirds(vm, v3)
            d, _ = thirds(vm, v4)
            e, _ = thirds(vm, v5)
            s.faces.append(Face(a, b, c, d, e, e, vm))

        for face in s.faces:
            face.divide(depth, depth)

    def breadth_first_traversal(s):
        pass

    def faces_at_level(s, level):
        for toplevel in s.faces:
            for face in toplevel.faces_at_level(level):
                yield face

    def depth_first_traversal(s):
        if level is None:
            for toplevel in s.faces:
                for face in toplevel:
                    yield face

    def __iter__(s):
        pass

    def vertex_count(s):
        return sum(face.vertex_count() for face in s.faces)

    def buffers(s, level=None):
        if level is None: level = s.depth
        verts = [(0, 0, 0)]
        color = [(0, 0, 0)]
        index = [0]
        # i = 0 is origin point
        i = 1
        for face in s.faces_at_level(level):
            verts.extend(face.vertices())
            color.extend([face.color]*7)
            # Indices corresponding to each vertex.
            a, b, c, d, e, f, m = [n+i for n in range(7)]
            index.extend([
                a, b, m,
                b, c, m,
                c, d, m,
                d, e, m,
                e, f, m,
                f, a, m,
                a, b, 0,
                b, c, 0,
                c, d, 0,
                d, e, 0,
                e, f, 0,
                f, a, 0,
            ])
            i += 7
        return verts, index, color
            

class Face:
    def __init__(s, a, b, c, d, e, f, m, color=None):
        s.id = ""
        # These are points in 3D space.
        s.a = a
        s.b = b
        s.c = c
        s.d = d
        s.e = e
        s.f = f
        s.m = m  # the middle point
        s.z = (0, 0, 0) # the origin point
        # These are links to other faces.
        s.flip_ab = None
        s.flip_bc = None
        s.flip_cd = None
        s.flip_de = None
        s.flip_ef = None
        s.flip_fa = None
        # These are inset faces, aka subdivisions.
        s.down_a = None
        s.down_b = None
        s.down_c = None
        s.down_d = None
        s.down_e = None
        s.down_f = None
        s.down_m = None
        # These are the incomplete faces in the corners after subdivision.
        s.over_a = None
        s.over_b = None
        s.over_c = None
        s.over_d = None
        s.over_e = None
        s.over_f = None
        s.over_m = None

        s.radius = 1
        if color is None:
            s.color = new_color()
        else:
            s.color = color
        s.level = None
        s.divisions = 0

    def faces_at_level(s, level):
        if s.level == level:
            yield s
        if s.divisions > 0:
            for division in s.subdivisions():
                for face in division:
                    if face.level == level:
                        yield face

    def __iter__(s):
        yield s
        if s.divisions > 0:
            for division in s.subdivisions():
                for face in division:
                    yield face

    def subdivisions(s):
        #return [s.down_a, s.down_b, s.down_c, s.down_d, s.down_e, s.down_f, s.down_m]
        return [
            s.down_a,
            s.down_b,
            s.down_c,
            s.down_d,
            s.down_e,
            s.down_f,
            s.down_m,
            #s.over_a,
            #s.over_b,
            #s.over_c,
            #s.over_d,
            #s.over_e,
            #s.over_f,
        ]


    def vertices(s):
        return [s.a, s.b, s.c, s.d, s.e, s.f, s.m]


    def divide(s, n_levels, depth):
        # Create the new faces by splitting this face's points in thirds.
        s.down_a = Face(*hexpoints(s.f, s.a, s.m))
        s.down_b = Face(*hexpoints(s.a, s.b, s.m))
        s.down_c = Face(*hexpoints(s.b, s.c, s.m))
        s.down_d = Face(*hexpoints(s.c, s.d, s.m))
        s.down_e = Face(*hexpoints(s.d, s.e, s.m))
        s.down_f = Face(*hexpoints(s.e, s.f, s.m))
        s.down_m = Face(*middle_hexpoints(s.a, s.b, s.c, s.d, s.e, s.f, s.m))

        # What to do about the incomplete corner hexes?
        # Those are shared between three parent faces.
        # We could just have lots of duplicates for right now.
        # The points would be in the right places.
        # There would just be too many of them.
        #s.over_a = Face(*over_hexpoints(s.m, s.a, s.f, s.b))
        #s.over_b = Face(*over_hexpoints(s.m, s.b, s.a, s.c))
        #s.over_c = Face(*over_hexpoints(s.m, s.c, s.b, s.d))
        #s.over_d = Face(*over_hexpoints(s.m, s.d, s.c, s.e))
        #s.over_e = Face(*over_hexpoints(s.m, s.e, s.d, s.f))
        #s.over_f = Face(*over_hexpoints(s.m, s.f, s.e, s.a))
        # We're going to do this in another pass.

        s.divisions = depth
        s.level = n_levels - depth
        if depth > 0:
            for face in s.subdivisions():
                face.divide(n_levels, depth-1)

    def link_internally(s):
        # Connect the sublevel of faces between themselves.
        s.down_a.flip_bc = s.down_b
        s.down_a.flip_cd = s.down_m
        s.down_a.flip_de = s.down_f

        s.down_b.flip_cd = s.down_c
        s.down_b.flip_de = s.down_m
        s.down_b.flip_ef = s.down_a

        s.down_c.flip_de = s.down_d
        s.down_c.flip_ef = s.down_m
        s.down_c.flip_fa = s.down_b

        s.down_d.flip_ef = s.down_e
        s.down_d.flip_fa = s.down_m
        s.down_d.flip_ab = s.down_c

        s.down_e.flip_fa = s.down_f
        s.down_e.flip_ab = s.down_m
        s.down_e.flip_bc = s.down_d

        s.down_f.flip_ab = s.down_a
        s.down_f.flip_bc = s.down_m
        s.down_f.flip_cd = s.down_e

        s.down_m.flip_fa = s.down_a
        s.down_m.flip_ab = s.down_b
        s.down_m.flip_bc = s.down_c
        s.down_m.flip_cd = s.down_d
        s.down_m.flip_de = s.down_e
        s.down_m.flip_ef = s.down_f

        # Just assume all other faces are already made and connected for now.
        # This will run into problems when we actually run it.
        # Other faces will not have been made at the point we try to access their attributes.
        s.down_a.flip_fa = s.flip_fa.down_d
        s.down_b.flip_ab = s.flip_fa.down_e
        s.down_c.flip_bc = s.flip_fa.down_f
        s.down_d.flip_cd = s.flip_fa.down_a
        s.down_e.flip_de = s.flip_fa.down_b
        s.down_f.flip_ef = s.flip_fa.down_c

        # TODO: incomplete connections

    def link_adjacent_faces(s):
        # In a second pass, after all faces have been created and divided,
        # connect each face's flip_xy links to its adjacent faces, creating
        # a traversable graph.
        pass

    def tris_face(s):
        return [
            (s.a, s.b, s.m),
            (s.b, s.c, s.m),
            (s.c, s.d, s.m),
            (s.d, s.e, s.m),
            (s.e, s.f, s.m),
            (s.f, s.a, s.m),
        ]

    def tris_stem(s):
        return [
            (s.a, s.b, s.z),
            (s.b, s.c, s.z),
            (s.c, s.d, s.z),
            (s.d, s.e, s.z),
            (s.e, s.f, s.z),
            (s.f, s.a, s.z),
        ]


# These functions will use triplets of cartesian coordinates for now.
# I'd like to switch to spherical coords later on.
def midpoint(a, b):
    """
    Return the point halfway between a and b.
    """
    return (
        (a[0]+b[0])/2,
        (a[1]+b[1])/2,
        (a[2]+b[2])/2 )


def thirds(a, b):
    """
    Return two points between a and b that split the line into thirds.
    Returns two values. The first is closer to a, and the second is closer to b.
    """
    aab = ( (2*a[0]+b[0])/3, (2*a[1]+b[1])/3, (2*a[2]+b[2])/3 )
    abb = ( (a[0]+b[0]*2)/3, (a[1]+b[1]*2)/3, (a[2]+b[2]*2)/3 )
    return aab, abb


def hexpoints(v1, v2, v3):
    """
    Return the seven points defining a hexagon inset in the given triangle.
    """
    # You'll have to see a diagram for this to make sense.
    f, a = thirds(v1, v2)
    b, c = thirds(v2, v3)
    d, e = thirds(v3, v1)
    m = midpoint(b, e)
    return a, b, c, d, e, f, m


def middle_hexpoints(pa, pb, pc, pd, pe, pf, m):
    """
    Return the points defining a hexagon centered within another hexagon.
    """
    a, _ = thirds(m, pa)
    b, _ = thirds(m, pb)
    c, _ = thirds(m, pc)
    d, _ = thirds(m, pd)
    e, _ = thirds(m, pe)
    f, _ = thirds(m, pf)
    return a, b, c, d, e, f, m


def over_hexpoints(parent_middle, new_middle, left, right):
    # This makess an incomplete hexagon.
    # But it still has to return 7 points, so it repeats.
    # This is all temporary until I find a better solution.
    z = (0, 0, 0)
    a, _ = thirds(new_middle, parent_middle)
    b, _ = thirds(new_middle, left)
    c, _ = thirds(new_middle, right)
    return a, b, c, z, z, z, new_middle


def over_penpoints(v1, v2, v3):
    # Create duplicate faces for top-level pentagons.
    z = (0, 0, 0)
    a, _ = thirds(v1, v2)
    b, _ = thirds(v1, v3)
    return a, b, v1, z, z, z, v1


def new_color():
    return np.random.random(3)
