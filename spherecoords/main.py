
import rocket
from rocket import aux
import numpy as np
from math import pi, sqrt
from vispy.gloo import IndexBuffer


def init():
    global program, camera, sphere, slate
    program = rocket.program("v.glsl", "f.glsl")
    camera = aux.View(fov=45)
    sphere = aux.Mover()
    slate = np.full((500, 500, 3), 128, dtype=np.uint8)
    camera.move(z=-4)


def generate():
    """
    Create a uv-mapped sphere using polar coordinates.
    """
    rad = []
    azi = []
    inc = []
    tex = []
    # 2*pi divided into however many parts
    c_azi = 20
    c_inc = 20
    s_azi = 2*pi/c_azi
    s_inc = 1*pi/c_inc
    a = -pi
    i = 0.0
    tx = 0
    ty = 0
    ind = np.zeros((c_azi*c_inc), dtype=np.uint32)
    n = 0
    for x in range(c_inc):
        for y in range(c_azi):
            rad.append(0.75)
            azi.append(a)
            inc.append(i)
            tex.append((tx, ty))
            ind[x*c_azi + y*2 if x%2==0 else (x-1)*c_azi + y*2 + 1] = n
            a += s_azi
            ty += s_azi
            n += 1
        i += s_inc
        tx += s_inc
    rad = np.array(rad, dtype=np.float32)
    azi = np.array(azi, dtype=np.float32)
    inc = np.array(inc, dtype=np.float32)
    tex = np.array(tex, dtype=np.float32)
    ind = IndexBuffer(ind)
    return rad, azi, inc, tex, ind


# The index doesn't work because triangle_strip needs to visit the same vertices
# twice. We need a different index strategy.
# Basically, we need to solve the tile-a-square-plane-with-triangle-strip
# problem before we can tackle this.
def uvsphere(radius, h, v):
    size = h*v
    index_count = size*2 - h*2  # hard to explain
    rad = np.full(size, radius, dtype=np.float32)
    azi = np.zeros(size, dtype=np.float32)
    inc = np.zeros(size, dtype=np.float32)
    tex = np.zeros((size, 2), dtype=np.float32)
    ind = np.zeros(index_count, dtype=np.uint32)
    azi_step = 2*pi/h
    inc_step = 1*pi/v
    tex_step = 1/size
    a = -pi
    i = 0.0
    x = 0.0
    y = 1.0
    for row in range(h):
        for col in range(v):
            azi[row*h+col] = a
            inc[row*h+col] = i
            tex[row*h+col, :] = x, y
            a += azi_step
            x += tex_step
        i += inc_step
        y -= tex_step * v
    # Generate indices for triangle_strip in another step.
    n1, n2 = 0, h
    for i in range(index_count):
        if i%2 == 0:
            ind[i] = n1
            n1 += 1
        else:
            ind[i] = n2
            n2 += 1
    return rad, azi, inc, tex, IndexBuffer(ind)


def icosahedron(r):
    rad = []
    azi = []
    inc = []
    # Top and bottom points, then ten vertices at (+/-) arctan(1/2), all spaced
    # evenly, alternating between high and low. (arctan(1/2) ~~ 0.4 radians)
    # Top and bottom points.
    rad.extend([r, r])
    azi.extend([0.0, 0.0])
    inc.extend([pi, 0.0])
    # The set of outside points.
    for i in [2*pi/3, pi/3]:
        a = 0.0
        for y in range(5):
            rad.append(r)
            azi.append(a)
            inc.append(i)
            a += 2*pi/5
    rad = np.array(rad, dtype=np.float32)
    azi = np.array(azi, dtype=np.float32)
    inc = np.array(inc, dtype=np.float32)
    return rad, azi, inc


@rocket.attach
def draw():
    program['rad'] = rad
    program['azi'] = azi
    program['inc'] = inc
    program['tex'] = tex
    program['modl'] = sphere.transform
    program['view'] = camera.transform
    program['proj'] = camera.proj
    program['slate'] = slate
    program['color'] = (0.0, 0.0, 0.0, 1.0)
    program.draw('triangle_strip', ind)
    program['color'] = (0.2, 0.3, 0.4, 1.0)
    program.draw('points')


@rocket.attach
def left_drag(start, end, delta):
    sphere.rotate(x=delta[0], y=delta[1])


@rocket.attach
def scroll(point, direction):
    camera.move(0, 0, direction/10)


@rocket.attach
def hover(point):
    global slate
    x, y = map(int, point)
    x, y = 500-y, x  # confusing
    x1, x2 = max(0, x-50), min(499, x+50)
    y1, y2 = max(0, y-50), min(499, y+50)
    slate[x1:x2, y1:y2, :] = 0
    raycast(point)


def raycast(screen_point):
    x, y = rocket.screen_to_world(screen_point)
    d = normalize(screen(x, y, -1.0))
    origin = np.array([0, 0, 0])
    center = np.array([0, 0, -4])
    intersect(origin, d, center, 0.75)


def intersect(origin, direction, center, radius):
    #print(direction)
    m = origin - center
    #print(m)  # distance from origin to sphere should change when zooming
    b = np.dot(m, direction)
    c = np.dot(m, m) - radius**2
    #print(b, c)

    discriminant = b**2 - c
    print(discriminant)
    if discriminant <= 0:
        print("miss")
    else:
        print("hit")


def screen(x, y, z):
    global sphere, camera
    invproj = np.linalg.inv(camera.proj)
    invview = np.linalg.inv(camera.transform)
    #print(invview)
    #invmodl = np.linalg.inv(sphere.transform)
    #x, y, _, _ = np.dot(invproj, [x, y, -1.0, 1.0])
    #x, y, z, _ = np.dot(invview, [x, y, -1.0, 0.0])
    #x, y, z, _ = np.dot(invmodl, [x, y, z, 0.0])
    v = [x, y, z, 1.0]
    #return np.dot(invview, np.dot(invproj, v))[0:3]  # remove w
    return np.dot(np.dot(v, invproj), invview)[0:3]  # remove w


def normalize(vector):
    mag = np.linalg.norm(vector, ord=1)
    return vector/mag


def main():
    global rad, azi, inc, tex, ind
    init()
    #rad, azi, inc, tex, ind = generate()
    rad, azi, inc, tex, ind = uvsphere(1, 20, 20)
    rocket.prep()
    rocket.launch()


if __name__ == '__main__':
    main()
