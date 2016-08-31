
import tools
import gen
import geometry
import numpy
from vispy.util import transforms
from vispy import gloo


class GameState:
    def __init__(self):
        self.view = gen.identity()
        self.proj = transforms.perspective(90.0, 1.0, 1.0, 20.0)

class GameObject:
    def __init__(self, model, trans):
        self.model = model
        self.trans = trans
        self.velocity = (0, 0)

game = GameState()
#game.view = tools.scale(game.view, 0.5)
game.view = numpy.dot(game.view, transforms.translate((0, 0, -3)))

ico = geometry.icosphere()
verts, index, lines = ico.triangles()
game.thing = GameObject(verts, gen.identity())
game.thing.index = gloo.IndexBuffer(index)



def damp(n):
    return n*0.95


def update(event):
    """Update the game. Called for every frame, usually sixty per second."""
    vx, vy = game.thing.velocity
    game.thing.trans = numpy.dot(game.thing.trans,
        transforms.rotate(vx, (0, 1, 0)))
    game.thing.trans = numpy.dot(game.thing.trans,
        transforms.rotate(vy, (1, 0, 0)))
    game.thing.velocity = damp(vx), damp(vy)


def draw(program):
    program['a_position'] = game.thing.model
    #program['a_coloring'] = color
    program['m_model'] = game.thing.trans
    program['m_view'] = game.view
    program['m_proj'] = game.proj
    program['u_color'] = (0.5, 0.6, 0.7)
    program.draw('triangles', gloo.IndexBuffer(index))
    program['u_color'] = (0.2, 0.3, 0.4)
    program.draw('lines', gloo.IndexBuffer(lines))
    program['u_color'] = (0.0, 0.0, 0.1)
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
    game.thing.velocity = (0-delta[0]*100, delta[1]*100)
    #game.thing.trans = numpy.dot(game.thing.trans,
        #transforms.rotate((0-delta[0]*50), (0, 1, 0)))
    #game.thing.trans = numpy.dot(game.thing.trans,
        #transforms.rotate(delta[1]*50, (1, 0, 0)))


def right_click_and_drag(start_point, end_point, delta):
    #print('right click and drag')
    game.thing.trans = numpy.dot(game.thing.trans,
        transforms.rotate(delta[1]*20, (0, 0, 1)))


def middle_click_and_drag(start_point, end_point, delta):
    #print('middle click and drag')
    game.thing.trans = numpy.dot(game.thing.trans,
        transforms.rotate((0-delta[0]*50), (0, 1, 0)))
    game.thing.trans = numpy.dot(game.thing.trans,
        transforms.rotate(delta[1]*50, (1, 0, 0)))


def scroll(point, direction):
    """Called when the mouse wheel scrolls up or down.

    point: the pair of (a, b) world coordinates showing where the scroll happened.
    direction: either +1 or -1 for scrolling in and out respectively.
    """
    #print('scroll')
    game.view = numpy.dot(game.view, transforms.translate((0, 0, direction)))


def hover(point):
    """Called when the mouse moves to a new point without holding any buttons."""
    #print('hover')


def key_press(key):
    """Called once when a key is pressed."""
    #print('key press')


def key_hold(keys):
    """Called once every frame while a key is held down."""
    #print('key hold')
