
from vispy import gloo, io
import rocket
import rocket.aux as aux
import icotree
import numpy as np


def main():
    global planet, camera, program, icosphere
    planet = aux.Mover()
    camera = aux.View(fov=45)
    program = aux.load_shaders('shaders/vertex.glsl', 'shaders/fragment.glsl')
    icosphere = icotree.Icosphere(1)

    rocket.prep(size=(512, 512))
    camera.move(z=(-6))
    planet.vel = aux.Velocity()
    planet.verts = icosphere.buffers()
    rocket.launch()


@rocket.attach
def update():
    """Update the game. Called for every frame, usually sixty per second."""
    planet.rotate(*tuple(planet.vel))
    planet.vel.damp()


@rocket.attach
def draw():
    program['a_position'] = planet.verts
    program['m_model'] = planet.transform
    program['m_view'] = camera.transform
    program['m_proj'] = camera.proj
    program['u_color'] = (0.0, 0.0, 0.1)
    program.draw('points')


@rocket.attach
def key_press(key):
    if key == 'R':
        pass


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
