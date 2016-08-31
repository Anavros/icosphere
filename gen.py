
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


def midpoint(v1, v2):
    (x1, y1, z1) = v1
    (x2, y2, z2) = v2
    return ((x2+x1)/2, (y2+y1)/2, (z2+z1)/2)


class Geometry:
    def __init__(self, n_verts, n_edges):
        self.v = np.array(shape=n_verts, dtype=np.float32)
        self.i = np.array(shape=n_edges, dtype=np.uint32)


def fancy_cube(x=1.0):
    return np.array([
        (-x, +x, +x), (+x, +x, +x),
        (-x, -x, +x), (+x, -x, +x),
        (-x, +x, -x), (+x, +x, -x),
        (-x, -x, -x), (+x, -x, -x),
    ], dtype=np.float32)
    # note: each vertex is connected to three vertices that have
    # exactly one different dimension.


def link(verts):
    links = {}
    for i1, v1 in enumerate(verts):
        n1 = plane(v1)
        links[i1] = set()
        for i2, v2 in enumerate(verts):
            n2 = plane(v2)
            dis = sum(distance(v1, v2))
            if (n1 == n2 and 1.5 <= dis <= 2.5) or (n1 != n2 and 1.5 <= dis <= 3.5):
                links[i1].add(i2)
    return links


def link_between(verts, a, b):
    links = {}
    dists = set()
    for i1, v1 in enumerate(verts):
        links[i1] = set()
        for i2, v2 in enumerate(verts):
            dis = sum(distance(v1, v2))
            if a <= dis <= b:
                links[i1].add(i2)
            dists.add(dis)
    print('dists')
    dists = list(dists)
    dists.sort()
    for d in dists:
        print(d)
    return links


def truncate(verts, links):
    new_links = {}
    new_verts = []
    vert_count = 0
    for i1, linkset in links.items():
        for i2 in linkset:
            v1 = verts[i1]
            v2 = verts[i2]
            mp = median(v1, v2, weight=2)
            new_verts.append(mp)
            vert_count += 1
            #new_links[vert_count] = links[v1]
    return np.array(new_verts, dtype=np.float32)


def black(verts):
    return np.full_like(verts, (0, 0, 0))


def plane(v):
    if v[0] == 0: # green
        return 'green'
    elif v[1] == 0: # blue
        return 'blue'
    elif v[2] == 0: # red
        return 'red'

def links_to_indices(links):
    indices = []
    for (i1, ls) in links.items():
        for i2 in ls:
            indices.append([i1, i2])
    return np.array(indices, dtype=np.uint32)
            

def distance(v1, v2):
    return tuple([abs(p2-p1) for p1, p2 in zip(v1, v2)])


def median(v1, v2, weight=1):
    return tuple([((p2*weight)+p1)/(weight+1) for p1, p2 in zip(v1, v2)])
    #return tuple([(p2+p1)/2 for p1, p2 in zip(v1, v2)])


def normalize(v):
    pass


def icosahedron():
    # built with 12 points, three flat rects, one in each plane
    # special golden mean constant
    t = ((1.0 + np.sqrt(5.0))) / 2.0
    return np.array([
        #(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0),
        #(0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
        #(t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1),
        (-1, t, 0), (1, t, 0), (1, -t, 0), (-1, -t, 0),  # red
        (0, -1, t), (0, 1, t), (0, 1, -t), (0, -1, -t),  # green
        (t, 0, -1), (t, 0, 1), (-t, 0, 1), (-t, 0, -1),  # blue
    ], dtype=np.float32)

# if random point has (_, _, 0) -> red, etc
# if red -> one connection to red, two to green, two to blue


def ico_color():
    return np.array([
        (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0),
        (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0),
        (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1),
    ], dtype=np.float32)


def ico_index(method='lines'):
    if method == 'lines':
        return np.array([
            0, 1,
#            1, 2,
            2, 3,
#            3, 0,
#
            4, 5,
#            5, 6,
            6, 7,
#            7, 4,
#
            8, 9,
#            9, 10,
            10, 11,
#            11, 8,

            0, 5,
            1, 5,
            0, 6,
            1, 6,
            2, 7,
            3, 7,
            2, 4,
            3, 4,

            0, 10,
            0, 11,
            3, 10,
            3, 11,
            1, 8,
            1, 9,
            2, 8,
            2, 9,

            4, 10,
            4, 9,
            5, 10,
            5, 9,
            6, 8,
            6, 11,
            7, 8,
            7, 11,
        ], dtype=np.uint32)
    elif method == 'triangles':
        return np.array([
            0, 11, 5,
            0, 5, 1,
            0, 1, 7,
            0, 7, 10,
            0, 10, 11,
            1, 5, 9,
            5, 11, 4,
            11, 10, 2,
            10, 7, 6,
            7, 1, 8,
            3, 4, 2,
            3, 2, 6,
            3, 6, 8,
            3, 8, 9,
            4, 9, 5,
            2, 4, 11,
            6, 2, 10,
            8, 6, 7,
            9, 8, 1,
        ], dtype=np.uint32)


#faces.Add(new TriangleIndices(0, 11, 5));
#faces.Add(new TriangleIndices(0, 5, 1));
#faces.Add(new TriangleIndices(0, 1, 7));
#faces.Add(new TriangleIndices(0, 7, 10));
#faces.Add(new TriangleIndices(0, 10, 11));
#
#// 5 adjacent faces
#faces.Add(new TriangleIndices(1, 5, 9));
#faces.Add(new TriangleIndices(5, 11, 4));
#faces.Add(new TriangleIndices(11, 10, 2));
#faces.Add(new TriangleIndices(10, 7, 6));
#faces.Add(new TriangleIndices(7, 1, 8));
#
#// 5 faces around point 3
#faces.Add(new TriangleIndices(3, 9, 4));
#faces.Add(new TriangleIndices(3, 4, 2));
#faces.Add(new TriangleIndices(3, 2, 6));
#faces.Add(new TriangleIndices(3, 6, 8));
#faces.Add(new TriangleIndices(3, 8, 9));
#
#// 5 adjacent faces
#faces.Add(new TriangleIndices(4, 9, 5));
#faces.Add(new TriangleIndices(2, 4, 11));
#faces.Add(new TriangleIndices(6, 2, 10));
#faces.Add(new TriangleIndices(8, 6, 7));
#faces.Add(new TriangleIndices(9, 8, 1));

#var t = (1.0 + Math.Sqrt(5.0)) / 2.0;
#addVertex(new Point3D(-1,  t,  0));
#addVertex(new Point3D( 1,  t,  0));
#addVertex(new Point3D(-1, -t,  0));
#addVertex(new Point3D( 1, -t,  0));
#
#addVertex(new Point3D( 0, -1,  t));
#addVertex(new Point3D( 0,  1,  t));
#addVertex(new Point3D( 0, -1, -t));
#addVertex(new Point3D( 0,  1, -t));
#
#addVertex(new Point3D( t,  0, -1));
#addVertex(new Point3D( t,  0,  1));
#addVertex(new Point3D(-t,  0, -1));
#addVertex(new Point3D(-t,  0,  1));
