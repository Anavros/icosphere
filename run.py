#!/usr/bin/env python3.4

import polyhedra
import rocket
import aux

planet = aux.Mover()
poly = polyhedra.Icosahedron()
camera = aux.View(fov=45)
camera.move(z=(-6))
program = aux.load_shaders('vertex.glsl', 'fragment.glsl')

def main():
    rocket.prep(title="???")
    planet.vel = aux.Velocity()
    reset()
    update_planet()
    rocket.launch()


def reset():
    global poly
    poly = polyhedra.Icosahedron()
    polyhedra.normalize(poly)


def update_planet():
    planet.verts, planet.index, planet.lines, planet.color = poly.construct_buffers()
    planet.index = aux.buffer(planet.index)
    planet.lines = aux.buffer(planet.lines)


@rocket.attach
def update():
    """Update the game. Called for every frame, usually sixty per second."""
    planet.rotate(*tuple(planet.vel))
    planet.vel.damp()


@rocket.attach
def draw():
    program['a_position'] = planet.verts
    program['a_coloring'] = planet.color

    program['m_model'] = planet.transform
    program['m_view'] = camera.transform
    program['m_proj'] = camera.proj

    program['u_color'] = (0.5, 0.6, 0.7)
    program.draw('triangles', planet.index)
    program['u_color'] = (0.2, 0.3, 0.4)
    program.draw('lines', planet.lines)
    program['u_color'] = (0.0, 0.0, 0.1)
    program.draw('points')


@rocket.attach
def key_press(key):
    if key == 'R':
        reset()
        update_planet()
    if key == 'T':
        polyhedra.tesselate(poly)
        update_planet()
    elif key == 'Y':
        polyhedra.hexify(poly)
        update_planet()
    elif key == 'U':
        polyhedra.normalize(poly)
        update_planet()


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
    camera.move(0, 0, direction)

main()
