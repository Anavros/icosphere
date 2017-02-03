
import rocket
from rocket import aux
import numpy as np
from math import pi


def init():
    global program, camera, sphere
    program = rocket.program("v.glsl", "f.glsl")
    camera = aux.View(fov=45)
    sphere = aux.Mover()
    camera.move(z=-6)


def generate():
    rad = []
    azi = []
    inc = []
    # 2*pi divided into however many parts
    c_azi = 18
    c_inc = 4
    s_azi = 2*pi/c_azi
    s_inc = 1*pi/c_inc
    a = -pi
    i = 0.0
    for x in range(c_inc):
        if x % 2 == 0:
            shift = 0
        else:
            shift = s_azi/2
        for y in range(c_azi):
            rad.append(0.75)
            azi.append(a+shift)
            inc.append(i)
            a += s_azi
        i += s_inc
    rad = np.array(rad, dtype=np.float32)
    azi = np.array(azi, dtype=np.float32)
    inc = np.array(inc, dtype=np.float32)
    return rad, azi, inc


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
    program['modl'] = sphere.transform
    program['view'] = camera.transform
    program['proj'] = camera.proj
    program.draw('points')


@rocket.attach
def left_drag(start, end, delta):
    sphere.rotate(x=delta[0], y=delta[1])


@rocket.attach
def scroll(point, direction):
    camera.move(0, 0, direction/10)


def main():
    global rad, azi, inc
    init()
    #rad, azi, inc = generate()
    rad, azi, inc = icosahedron(0.75)
    rocket.prep()
    rocket.launch()


if __name__ == '__main__':
    main()
