
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
    regen()
    refresh()
    rocket.launch()


def regen():
    global shape
    shape = geom.Triangle(*base, depth=depth)


def refresh():
    global shape, verts, index, color
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
        regen()
        refresh()
    if key == 'T':
        depth += 1
        regen()
        refresh()


def recolor(root, point):
    for tri in root.traverse():
        d = tri.distance(point)/2
        tri.color = (d, d, d)
    refresh()


def highlight(root, point):
    sub = root.locate(point)
    if sub is not None:
        print(sub)
        sub.color = (1.0, 1.0, 1.0)
        refresh()
        print("Found")
    else:
        print("Not Found")


def rootdistance(root, point):
    print(root.distance(point))


@rocket.attach
def left_click(point):
    global shape
    point = rocket.screen_to_world(point)
    #rootdistance(shape, point)
    #highlight(shape, point)
    recolor(shape, point)


if __name__ == '__main__':
    main()
