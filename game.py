
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
game.view = tools.scale(game.view, 0.5)

ico = gen.icosphere()
verts, index = ico.data()
game.thing = GameObject(verts, gen.identity())
game.thing.index = gloo.IndexBuffer(index)

#game.thing = GameObject(gen.icosahedron(), gen.identity())
#links = gen.link(game.thing.model)
#game.thing.model, links = gen.truncate(game.thing.model, links)
#game.thing.index = gloo.IndexBuffer(gen.links_to_indices(links))
#game.thing.color = gen.black(game.thing.model)


def update(event):
    """Update the game. Called for every frame, usually sixty per second."""
    #game.thing.trans = numpy.dot(game.thing.trans, transforms.rotate(0.2, (0.7, 1, 0.3)))


def draw(program):
    program['a_position'] = game.thing.model
    #program['a_coloring'] = game.thing.color
    program['m_model'] = game.thing.trans
    program['m_view'] = game.view
    program.draw('lines', game.thing.index)
    program.draw('points')


def left_click(point):
    """Perform these actions when the left mouse button is clicked."""
    #print('left click')
    game.thing.trans = numpy.dot(game.thing.trans, transforms.rotate(15, (0, 1, 1)))
    

def right_click(coord):
    #print('right click')
    pass


def middle_click(coord):
    #print('middle click')
    pass


def left_click_and_drag(start_point, end_point, delta):
    #print('left click and drag')
    game.thing.trans = numpy.dot(game.thing.trans,
        transforms.rotate((0-delta[0]*50), (0, 1, 0)))
    game.thing.trans = numpy.dot(game.thing.trans,
        transforms.rotate(delta[1]*50, (1, 0, 0)))


def right_click_and_drag(start_point, end_point, delta):
    #print('right click and drag')
    game.thing.trans = numpy.dot(game.thing.trans,
        transforms.rotate(delta[1]*20, (0, 0, 1)))


def middle_click_and_drag(start_point, end_point, delta):
    #print('middle click and drag')
    pass


def scroll(point, direction):
    """Called when the mouse wheel scrolls up or down.

    point: the pair of (a, b) world coordinates showing where the scroll happened.
    direction: either +1 or -1 for scrolling in and out respectively.
    """
    #print('scroll')
    game.view = tools.scale(game.view, 1+direction/10)


def hover(point):
    """Called when the mouse moves to a new point without holding any buttons."""
    #print('hover')


def key_press(key):
    """Called once when a key is pressed."""
    #print('key press')


def key_hold(keys):
    """Called once every frame while a key is held down."""
    #print('key hold')
