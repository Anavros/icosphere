
import numpy


def identity():
    return numpy.eye(4, dtype=numpy.float32)


def point():
    return numpy.array([
        (0.0, 0.0),
    ], dtype=numpy.float32)


def square():
    return numpy.array([
        (-0.2, +0.2), (+0.2, +0.2),
        (-0.2, -0.2), (+0.2, -0.2),
    ], dtype=numpy.float32)


def cube(x=1.0):
    return numpy.array([
        (-x, +x, +x), (+x, +x, +x),
        (-x, -x, +x), (+x, -x, +x),
        (-x, +x, -x), (+x, +x, -x),
        (-x, -x, -x), (+x, -x, -x),
    ], dtype=numpy.float32)


def icosahedron():
    # built with 12 points, three flat rects, one in each plane
    # special theta constant
    t = ((1.0 + numpy.sqrt(5.0))) / 2.0
    return numpy.array([
        #(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0),
        #(0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
        #(t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1),
        (-1, t, 0), (1, t, 0), (1, -t, 0), (-1, -t, 0),
        (0, -1, t), (0, 1, t), (0, 1, -t), (0, -1, -t),
        (t, 0, -1), (t, 0, 1), (-t, 0, 1), (-t, 0, -1),
    ], dtype=numpy.float32)


def ico_color():
    return numpy.array([
        (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0),
        (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0),
        (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1),
    ], dtype=numpy.float32)


def ico_index(method='lines'):
    if method == 'lines':
        return numpy.array([
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
        ], dtype=numpy.uint32)
    elif method == 'triangles':
        return numpy.array([
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
        ], dtype=numpy.uint32)

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
