
import rocket
import numpy as np
from vispy.gloo import Texture2D


def init():
    global program, pos, tex, slate
    program = rocket.program('v.glsl', 'f.glsl')
    pos = np.array([
        (-1, +1), (+1, +1),
        (-1, -1), (+1, -1),
    ], dtype=np.float32)
    tex = np.array([
        (0, 1), (1, 1),
        (0, 0), (1, 0),
    ], dtype=np.float32)
    slate = np.full((500, 500, 3), 128, dtype=np.uint8)


def generate_sphere():
    """
    Create a 
    """


def main():
    init()
    rocket.prep()
    rocket.launch()


@rocket.attach
def draw():
    program['pos'] = pos
    program['tex'] = tex
    program['slate'] = slate
    program.draw('triangle_strip')


@rocket.attach
def hover(point):
    global slate
    x, y = map(int, point)
    x, y = 500-y, x  # confusing
    x1, x2 = max(0, x-5), min(499, x+5)
    y1, y2 = max(0, y-5), min(499, y+5)
    slate[x1:x2, y1:y2, :] = 0


if __name__ == '__main__':
    main()
