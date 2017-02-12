

class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Face:
    """
    Triangular face that recursively subdivides itself upon creation. Performs
    `recursion_depth` subdivisions. Each sub-face is connected in a graph.
    Optionally pass in three adjacent faces for the sub-faces of this graph to
    connect to the sub-faces of those graphs. If done in three-dimensional
    shapes this can create a fully-connected regular grid.
    """
    def __init__(self, a, b, c, adj_ab=None, adj_bc=None, adj_ca=None, recursion_depth=0):
        self.a = a
        self.b = b
        self.c = c
        self.adjacent_ab = adj_ab
        self.adjacent_bc = adj_bc
        self.adjacent_ca = adj_ca
        if recursion_depth > 0:
            self.interior_a = Face()
            self.interior_b = Face()
            self.interior_c = Face()
            self.interior_m = Face()
        else:
            self.interior_a = None
            self.interior_b = None
            self.interior_c = None
            self.interior_m = None

    def all_faces(self):
        pass



class UpperTriangle(Triangle):
    def __init__(self, parent, a, b, c, ab, bc, ca, depth):
        Triangle.__init__(self)
        self.point_a = a
        self.point_b = b
        self.point_c = c
        self.inner_a = None
        self.inner_b = None
        self.inner_c = None
        self.inner_m = None
        self.outer_ab = ab
        self.outer_bc = bc
        self.outer_ca = ca
        self.mark = "upper"
        if depth > 0:
            self.subdivide(depth-1)

    def subdivide(self, depth):
        ab = midpoint(t.a, t.b)
        bc = midpoint(t.b, t.c)
        ca = midpoint(t.c, t.a)
        self.inner_a = LowerTriangle(t.a, ab, ca, depth)
        self.inner_b = LowerTriangle(ab, t.b, bc, depth)
        self.inner_c = LowerTriangle(ca, bc, t.c, depth)
        self.inner_m = UpperTriangle(ca, ab, bc,  depth)
        if self.outer_ab is not None:
            # This won't work because not all triangles will be subdivided by
            # the time this runs.
            self.inner_a.outer_ab = self.outer_ab.inner_f.outer_fe
        if self.outer_bc is not None:
            pass
        if self.outer_ca is not None:
            pass


class LowerTriangle(Triangle):
    def __init__(self):
        Triangle.__init__(self)
        self.d = None
        self.e = None
        self.f = None
        self.next_de = None
        self.next_ef = None
        self.next_fd = None
        self.mark = "lower"
        if depth > 0:
            self.subdivide(depth-1)

    def subdivide(self, depth):
        pass
