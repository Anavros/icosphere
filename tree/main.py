
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
    global shape, verts, index, color
    shape = geom.Triangle(*base, depth=depth)
    verts, index, color = geom.bottom(shape)


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


@rocket.attach
def left_click(point):
    point = rocket.screen_to_world(point)
    print(point)
    print(point in shape)


if __name__ == '__main__':
    main()
