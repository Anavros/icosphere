
import tools


class GameState:
    def __init__(self):
        """Called once when you make a new GameState().
        Ex: game = GameState() -> calls __init__()
        """
        self.view = tools.identity()
        self.player = GameObject(tools.square(), tools.identity())
        self.cursor = GameObject(tools.point(), tools.identity())
        self.projectiles = []

class GameObject:
    def __init__(self, model, place, vector=(0.0, 0.1)):
        self.model = model
        self.place = place
        self.vector = vector

# Global State Variable
# You can call this variable, and access anything inside of it, from any one of
# the functions below. Example: game.player_ship ... and so on.
game = GameState()


def update(event):
    """Update the game. Called for every frame, usually sixty per second."""
    for proj in game.projectiles:
        proj.place = tools.move(proj.place, proj.vector)


def draw(program):
    tools.draw(game.player.model, game.player.place, game.view, program)
    tools.draw(game.cursor.model, game.cursor.place, game.view, program)
    for proj in game.projectiles:
        tools.draw(proj.model, proj.place, game.view, program)


def left_click(coord):
    """Perform these actions when the left mouse button is clicked."""
    print('left click')
    game.projectiles.append(GameObject(
        tools.point(), game.player.place, vector=(0.0, 0.1)))
    #game.player.place = tools.move(game.player.place, (0.1, 0.1))
    

def right_click(coord):
    print('right click')


def middle_click(coord):
    print('middle click')


def left_click_and_drag(start_point, end_point, delta):
    print('left click and drag')
    game.player.place = tools.move(game.player.place, delta)


def right_click_and_drag(start_point, end_point, delta):
    print('right click and drag')
    game.player.place = tools.rotate(game.player.place, 90*delta[0])


def middle_click_and_drag(start_point, end_point, delta):
    print('middle click and drag')
    game.player.place = tools.scale(game.player.place, 1+delta[1])


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
    game.cursor.place = tools.move(tools.identity(), point)


def key_press(key):
    """Called once when a key is pressed."""
    print('key press')


def key_hold(keys):
    """Called once every frame while a key is held down."""
    print('key hold')
