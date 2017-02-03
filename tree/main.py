
import rocket
from rocket import aux
from vispy import gloo, io
import numpy as np

import geom

program = rocket.program('v.glsl', 'f.glsl')
base = [
    ( 0.0, +1.0,),
    (-1.0, -1.0,),
    (+1.0, -1.0,),
]
tree = geom.Triangle(*base, depth=1)
#geom.count(tree)
buff = geom.buffers(tree)


def main():
    rocket.prep()
    rocket.launch()


@rocket.attach
def draw():
    program['pos'] = buff
    program.draw('triangles')


@rocket.attach
def key_press(key):
    pass


if __name__ == '__main__':
    main()
