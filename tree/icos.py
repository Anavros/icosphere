
from geom import Triangle


# TODO: Connect faces for top level of traversal graph.
class Icosahedron:
    def __init__(self, depth):
        """
        Generate the twenty faces of the icosahedron. Each face is a recursive
        triangle structure. Triangles subdivide on creation, to level `depth`.
        Faces are organized into a graph at the top level. Each face is a node
        on the graph. Connections represent adjacent faces. This allows walks to
        be performed on the shape without worrying about three-dimensional
        representations.
        """
        t = ((1.0 + np.sqrt(5.0))) / 2.0
        v = [
            (-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0),
            (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
            (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1),
        ]
        f = [
            (0, 11,  5), (0,  5,  1), (0,  1,  7), (0,  7, 10), (0, 10, 11),
            (2, 11, 10), (4,  5, 11), (9,  1,  5), (8,  7,  1), (6, 10,  7),
            (4,  9,  5), (9,  8,  1), (8,  6,  7), (6,  2, 10), (2,  4, 11),
            (3,  9,  4), (3,  4,  2), (3,  2,  6), (3,  6,  8), (3,  8,  9),
        ]
        self.faces = []
        for triplet in v:
            self.faces.append(Triangle(*triplet, depth))

    def traverse(self):
        """
        Yield each leaf-triangle in order. Used to iterate over every triangle
        when adjacencies and distances are not important.
        """
