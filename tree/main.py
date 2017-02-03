
import rocket
from rocket import aux
from vispy import gloo
import numpy as np

import geom

program = rocket.program('v.glsl', 'f.glsl')
base = [
    ( 0.0, +1.0,),
    (-1.0, -1.0,),
    (+1.0, -1.0,),
]
depth = 0


def main():
    rocket.prep()
    refresh()
    rocket.launch()


def refresh():
    global verts, index, color
    verts, index, color = geom.bottom(geom.Triangle(*base, depth=depth))


@rocket.attach
def draw():
    program['pos'] = verts
    program['col'] = color
    program.draw('triangles', gloo.IndexBuffer(index))


@rocket.attach
def key_press(key):
    global depth
    if key == 'R':
        depth = 0
        refresh()
    if key == 'T':
        depth += 1
        refresh()


if __name__ == '__main__':
    main()
