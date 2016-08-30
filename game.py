
import tools
import gen
import numpy
from vispy.util import transforms
from vispy import gloo


class GameState:
    def __init__(self):
        self.view = gen.identity()

class GameObject:
    def __init__(self, model, trans):
        self.model = model
        self.trans = trans

game = GameState()
game.thing = GameObject(gen.icosahedron(), gen.identity())
game.thing.index = gloo.IndexBuffer(gen.ico_index())
game.thing.color = gen.ico_color()


def update(event):
    """Update the game. Called for every frame, usually sixty per second."""


def draw(program):
    program['a_position'] = game.thing.model
    program['a_coloring'] = game.thing.color
    program['m_model'] = game.thing.trans
    program['m_view'] = game.view
    program.draw('lines', game.thing.index)


def left_click(point):
    """Perform these actions when the left mouse button is clicked."""
    print('left click')
    game.thing.trans = numpy.dot(game.thing.trans, transforms.rotate(15, (0, 1, 1)))
    

def right_click(coord):
    print('right click')


def middle_click(coord):
    print('middle click')


def left_click_and_drag(start_point, end_point, delta):
    print('left click and drag')
    game.thing.trans = numpy.dot(game.thing.trans,
        transforms.rotate((0-delta[0]*50), (0, 1, 0)))
    game.thing.trans = numpy.dot(game.thing.trans,
        transforms.rotate(delta[1]*50, (1, 0, 0)))


def right_click_and_drag(start_point, end_point, delta):
    print('right click and drag')
    game.thing.trans = numpy.dot(game.thing.trans,
        transforms.rotate(delta[1]*20, (0, 0, 1)))


def middle_click_and_drag(start_point, end_point, delta):
    print('middle click and drag')


def scroll(point, direction):
    """Called when the mouse wheel scrolls up or down.

    point: the pair of (a, b) world coordinates showing where the scroll happened.
    direction: either +1 or -1 for scrolling in and out respectively.
    """
    print('scroll')
    game.view = tools.scale(game.view, 1+direction/10)


def hover(point):
    """Called when the mouse moves to a new point without holding any buttons."""
    print('hover')


def key_press(key):
    """Called once when a key is pressed."""
    print('key press')


def key_hold(keys):
    """Called once every frame while a key is held down."""
    print('key hold')
