#!/usr/bin/env python3.4

import polyhedra
import rocket
import aux
from vispy import gloo, io
from uuid import uuid4
import os

planet = aux.Mover()
poly = polyhedra.Icosahedron()
camera = aux.View(fov=45)
camera.move(z=(-6))
program = aux.load_shaders('vertex.glsl', 'fragment.glsl')
#pic_dir = str(uuid4())
pic_n = 0
#go = False
#os.mkdir(os.path.join('screenshots', pic_dir))
#print('made directory', os.path.join('screenshots', pic_dir))

def main():
    rocket.prep(title="???", size=(512, 512))
    planet.vel = aux.Velocity()
    reset()
    update_planet()
    rocket.launch()


def profile():
    poly = polyhedra.Icosahedron()
    poly.tesselate()
    poly.tesselate()
    poly.hexify()
    poly.hexify()
    poly.normalize()


def reset():
    global poly
    poly = polyhedra.Icosahedron()
    poly.normalize()


def update_planet():
    planet.verts, planet.color, planet.index, planet.lines, planet.sides = poly.buffers()
    planet.sides = aux.buffer(planet.sides)
    planet.index = aux.buffer(planet.index)
    planet.lines = aux.buffer(planet.lines)


def screenshot():
    output = gloo.wrappers.read_pixels()
    global pic_n
    io.imsave(os.path.join('screenshots', '{}.png'.format(pic_n)), output)
    print('screenshot saved as screenshots/{}.png'.format(pic_n))
    pic_n += 1


@rocket.attach
def update():
    """Update the game. Called for every frame, usually sixty per second."""
    #global pic_n
    planet.rotate(*tuple(planet.vel))
    planet.vel.damp()
    #if go and pic_n < 256: screenshot()
    #planet.rotate(x=1.40625, y=1.40625)


@rocket.attach
def draw():
    program['a_position'] = planet.verts
    program['a_coloring'] = planet.color

    program['m_model'] = planet.transform
    program['m_view'] = camera.transform
    program['m_proj'] = camera.proj

    program['u_color'] = (0.5, 0.6, 0.7); program.draw('triangles', planet.index)
    program['u_color'] = (0.4, 0.5, 0.6); program.draw('triangles', planet.sides)
    program['u_color'] = (0.2, 0.3, 0.4); program.draw('lines', planet.lines)
    program['u_color'] = (0.0, 0.0, 0.1); program.draw('points')


@rocket.attach
def key_press(key):
    if key == 'R':
        reset()
        update_planet()
    if key == 'T':
        poly.tesselate()
        update_planet()
    elif key == 'Y':
        poly.hexify()
        update_planet()
    elif key == 'U':
        poly.normalize()
        update_planet()
    elif key == 'E':
        poly.extrude()
        update_planet()
    elif key == 'S':
        screenshot()
    elif key == 'N':
        planet.rotate(x=22.5, y=22.5)
    #elif key == 'G':
        #global go
        #go = True


@rocket.attach
def left_drag(start, end, delta):
    planet.vel.accel(x=delta[0]/5, y=delta[1]/5)


@rocket.attach
def right_drag(start, end, delta):
    planet.rotate(z=(0-delta[1])/2)


@rocket.attach
def middle_drag(start, end, delta):
    planet.rotate(x=delta[0], y=delta[1])
    planet.vel.decel(100, 100, 100)


@rocket.attach
def scroll(point, direction):
    camera.move(0, 0, direction/10)

if __name__ == '__main__':
    main()
    #import cProfile as prof
    #prof.run('profile()')
