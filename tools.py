

from vispy import gloo
from vispy.util import transforms
import numpy

from constants import WIDTH, HEIGHT


def screen_to_world(coords):
    (x, y) = coords
    a = ((x/WIDTH)*2)-1
    b = -(((y/HEIGHT)*2)-1)
    return (a, b)


def world_to_screen(coords):
    (a, b) = coords
    x = ((a+1)/2) * WIDTH
    y = ((-b+1)/2) * HEIGHT
    return (x, y)


def move(mat, vec2):
    return numpy.dot(mat, transforms.translate((vec2[0], vec2[1], 0)))


def rotate(mat, angle):
    # weird center of rotation
    return numpy.dot(mat, transforms.rotate(angle, (0, 0, 1)))


def scale(mat, factor):
    return numpy.dot(mat, transforms.scale((factor, factor, 0)))


def draw(mat, place, view, program):
    program['a_position'] = gloo.VertexBuffer(mat)
    program['m_model'] = place
    program['m_view'] = view
    program.draw('points')


def build_program(v_path, f_path):
    """Load shader programs as strings."""
    with open(v_path, 'r') as v_file:
        v_string = v_file.read()
    with open(f_path, 'r') as f_file:
        f_string = f_file.read()
    return gloo.Program(v_string, f_string)
