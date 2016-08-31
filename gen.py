
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


class Vert:
    def __init__(self, x, y, z, i=None):
        self.x = x
        self.y = y
        self.z = z
        self.i = i

    def __iter__(self):
        for n in [self.x, self.y, self.z]:
            yield n

    def __eq__(self, vert):
        return self.x==vert.x and self.y==vert.y and self.z==vert.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))


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


class Geometry:
    def __init__(self):
        self.edges = set()

    def connect(self, v1, v2):
        self.edges.add(Edge(v1, v2))

    def data(self):
        v_count = 0
        i_count = 0
        verts = np.zeros(shape=(len(self.edges)*2, 3), dtype=np.float32)
        index = np.zeros(shape=(len(self.edges), 2), dtype=np.uint32)
        for v1, v2 in self.edges:
            i1, i2 = v_count, v_count+1
            verts[i1, :] = tuple(v1)
            verts[i2, :] = tuple(v2)
            index[i_count] = (i1, i2)
            v_count += 2
            i_count += 1
        return verts, index


def icosphere():
    t = ((1.0 + np.sqrt(5.0))) / 2.0
    verts = [
        (-1, t, 0), (1, t, 0), (1, -t, 0), (-1, -t, 0),  # red
        (0, -1, t), (0, 1, t), (0, 1, -t), (0, -1, -t),  # green
        (t, 0, -1), (t, 0, 1), (-t, 0, 1), (-t, 0, -1),  # blue
    ]
    edges = [
        (0, 1),
        (2, 3),
        (4, 5),
        (6, 7),
        (8, 9),
        (10, 11),
        (0, 5),
        (1, 5),
        (0, 6),
        (1, 6),
        (2, 7),
        (3, 7),
        (2, 4),
        (3, 4),
        (0, 10),
        (0, 11),
        (3, 10),
        (3, 11),
        (1, 8),
        (1, 9),
        (2, 8),
        (2, 9),
        (4, 10),
        (4, 9),
        (5, 10),
        (5, 9),
        (6, 8),
        (6, 11),
        (7, 8),
        (7, 11),
    ]
    geo = Geometry()
    for v1, v2 in edges:
        geo.connect(verts[v1], verts[v2])
    return geo


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

#verts, index = ico.data('triangles')

def fantasy(icosphere):
    new = Geometry()
    for v1 in icosphere.verts:
        first, last = None, None
        for v2 in icosphere.edges[v1]:
            midpoint = median(v1, v2, weight=2)
            new.add(midpoint)
            new.connect(midpoint, v2)
            if first is None:
                first = midpoint
            if last is not None:
                new.connect(midpoint, last)
        new.connect(midpoint, first) # whatever midpoint is set to during last loop
    return new


def truncate(verts, links):
    new_links = {}
    new_verts = np.zeros((len(verts)*5, 3), dtype=np.float32)
    pointer = 0
    for i1, linkset in links.items():
        v1 = verts[i1]
        # for every one of these, we'll end up with 5 new ones
        # unless there are hexes
        # in which case we'll get 6? Actually, every vertex
        # after the first truncation has three connections
        first_midpoint = None
        last_midpoint = None
        for i2 in linkset:
            v2 = verts[i2]
            mp = median(v1, v2, weight=2)
            new_verts[pointer] = mp # 0
            # index of v2 is # 1
            # index of ?
            pointer += 1

            new_links[mp] = set()
            new_links[mp].add(v2)
            if last_midpoint is not None:
                if first_midpoint is None:
                    first_midpoint = mp
                new_links[mp].add(last_midpoint)
                last_midpoint = mp
        new_links[mp].add(first_midpoint)

    render = {}
    for l1, lns in new_links.items():
        i1 = new_verts.index(l1)
        render[i1] = set()
        for l2 in lns:
            i2 = new_verts.index(l2)
            render[i1].add(i2)
    return np.array(new_verts, dtype=np.float32), render


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
