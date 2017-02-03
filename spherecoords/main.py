
import rocket
import numpy as np
from math import pi


def init():
    global program
    program = rocket.program("v.glsl", "f.glsl")


def generate():
    global rad, azi, inc
    rad = []
    azi = []
    inc = []
    # 2*pi divided into however many parts
    c_azi = 6
    c_inc = 12
    s_azi = 2*pi/c_azi
    s_inc = 1*pi/c_inc
    a = -pi
    i = 0.0
    for _ in range(c_inc):
        for _ in range(c_azi):
            rad.append(0.75)
            azi.append(a)
            inc.append(i)
            a += s_azi
        i += s_inc
    rad = np.array(rad, dtype=np.float32)
    azi = np.array(azi, dtype=np.float32)
    inc = np.array(inc, dtype=np.float32)


@rocket.attach
def draw():
    program['rad'] = rad
    program['azi'] = azi
    program['inc'] = inc
    program.draw('points')


def main():
    init()
    generate()
    rocket.prep()
    rocket.launch()


if __name__ == '__main__':
    main()
