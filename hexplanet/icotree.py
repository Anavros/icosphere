

class Face:
    def __init__(s, a, b, c, d, e, f, m):
        # These are points in 3D space.
        s.a = a
        s.b = b
        s.c = c
        s.d = d
        s.e = e
        s.f = f
        s.m = m  # the middle point
        s.z = None  # (0, 0, 0), the origin point
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

        s.radius = 1
        s.color = None

    def divide(s):
        # Create the new faces by splitting this face's points in thirds.
        s.down_a = Face(*hexpoints(s.f, s.a, s.m))
        s.down_b = Face(*hexpoints(s.a, s.b, s.m))
        s.down_c = Face(*hexpoints(s.b, s.c, s.m))
        s.down_d = Face(*hexpoints(s.c, s.d, s.m))
        s.down_e = Face(*hexpoints(s.d, s.e, s.m))
        s.down_f = Face(*hexpoints(s.e, s.f, s.m))
        s.down_m = Face(*middle_hexpoints(s.a, s.b, s.c, s.d, s.e, s.f, s.m))

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


def midpoint(a, b):
    pass


def thirds(a, b):
    pass


def hexpoints(clockwise, anticlock, middle):
    # You'll have to see a diagram for this to make sense.
    f, a = thirds(clockwise, anticlock)
    b, c = thirds(anticlock, middle)
    d, e = thirds(middle, clockwise)
    m = midpoint(b, e)
    return a, b, c, d, e, f, m


def middle_hexpoints(pa, pb, pc, pd, pe, pf, m):
    a, _ = thirds(m, pa)
    b, _ = thirds(m, pb)
    c, _ = thirds(m, pc)
    d, _ = thirds(m, pd)
    e, _ = thirds(m, pe)
    f, _ = thirds(m, pf)
    return a, b, c, d, e, f, m
