
import rocket
import numpy as np
from math import pi


program = rocket.program("v.glsl", "f.glsl")
ang = []
rad = []
phi = []
# 2*pi divided into however many parts
top = 2*pi
n_lat = 6
n_lon = 12
s_lat = top/n_lat
s_lon = top/n_lon
n = 0.0
p = 0.0
for _ in range(n_lat):
    for _ in range(n_lon):
        ang.append(n)
        rad.append(0.75)
        phi.append(p)
        n += s_lon
    p += s_lat
ang = np.array(ang, dtype=np.float32)
rad = np.array(rad, dtype=np.float32)
phi = np.array(rad, dtype=np.float32)


def main():
    rocket.prep()
    rocket.launch()


@rocket.attach
def draw():
    program['rad'] = rad
    program['ang'] = ang
    program['phi'] = phi
    program.draw('points')


if __name__ == '__main__':
    main()
