
"""
A high-level opengl wrapper built around vispy.

The idea is to have one module to import that exposes just enough functionality
to have good access to opengl.

Essential Functions:
* Wrap vispy events so that they include more useful information.
    * Notably the draw function needs to contain the program.
    * Otherwise expanding and building upon basic events.
    * E.g. turning screen coordinates to world coordinates.
* Enable an update() function to run every frame.
    * A timer to call the function every frame.
* Simplify the opengl interface while still allowing low-level access.
    * Functions to simplify transformations and matrices.
    * Default settings to include transparency and depth buffering.
    * Maintain full access to the shader program oo interface.
* Possible integration with the gui toolkit.

So reasonably speaking, we could split this up into a few seperate tools.
One kit to wrap events, one to handle transformations, and one for drawing shortcuts.
But keep the program and canvas in the user's program?
"""

from vispy import app, gloo, io
from vispy.gloo import gl
import numpy as np
app.use_app('glfw')

HELD_KEYS = []
DEFAULT_BINDING = lambda:None
BINDINGS = {
    'draw':         DEFAULT_BINDING,
    'update':       DEFAULT_BINDING,
    'left_click':   DEFAULT_BINDING,
    'right_click':  DEFAULT_BINDING,
    'middle_click': DEFAULT_BINDING,
    'left_drag':    DEFAULT_BINDING,
    'right_drag':   DEFAULT_BINDING,
    'middle_drag':  DEFAULT_BINDING,
    'scroll':       DEFAULT_BINDING,
    'hover':        DEFAULT_BINDING,
    'key_press':    DEFAULT_BINDING,
    'key_hold':     DEFAULT_BINDING,
}


def bind(func):
    if func.__name__ not in BINDINGS.keys():
        raise ValueError("Unknown event: {}. Please use one of {}".format(
            func.name, BINDINGS.keys()))
    BINDINGS[func.__name__] = func


def start(canvas, program):
    # Initialization
    # Enables transparency and depth buffering.
    gl.glEnable(gl.GL_BLEND)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gloo.set_state(clear_color=(1, 1, 1, 1), depth_test=True)

    # Important Variables
    # Accessible in the below functions as closures.
    canvas = app.Canvas(title=TITLE, size=SIZE, keys='interactive')
    program = tools.build_program("vertex.glsl", "fragment.glsl")
    timer = app.Timer()

    # Event Handling Functions
    def on_draw(event):
        gloo.clear(color=True, depth=True)
        BINDINGS['draw'](program)
    canvas.connect(on_draw)

    def on_update(event):
        if held_keys: BINDINGS['key_hold'](held_keys)
        BINDINGS['key_hold'](event)
        canvas.update()
    timer.connect(on_update)

    def on_mouse_press(event):
        pass
    canvas.connect(on_mouse_press)

    def on_mouse_release(event):
        trail = event.trail()
        if trail is None or len(trail) <= 1:
            if event.button == 1:
                BINDINGS['left_click'](event.pos)
            elif event.button == 2:
                BINDINGS['right_click'](event.pos)
            elif event.button == 3:
                BINDINGS['middle_click'](event.pos)
        else:
            pass
    canvas.connect(on_mouse_release)

    def on_mouse_double_click(event):
        if event.last_event.button == 1:
            BINDINGS['left_click'](event.pos)
        elif event.last_event.button == 2:
            BINDINGS['right_click'](event.pos)
        elif event.last_event.button == 3:
            BINDINGS['middle_click'](event.pos)
    canvas.connect(on_mouse_double_click)

    def on_mouse_move(event):
        if event.button is None:
            BINDINGS['hover'](tools.screen_to_world(event.pos))
        else:
            (a1, b1) = tools.screen_to_world(event.last_event.pos)
            (a2, b2) = tools.screen_to_world(event.pos)
            (da, db) = (a2-a1, b2-b1)
            if event.button == 1:
                BINDINGS['left_drag']((a1, b1), (a2, b2), (da, db))
            elif event.button == 2:
                BINDINGS['right_drag']((a1, b1), (a2, b2), (da, db))
            elif event.button == 3:
                BINDINGS['middle_drag']((a1, b1), (a2, b2), (da, db))
    canvas.connect(on_mouse_move)

    def on_mouse_wheel(event):
        BINDINGS['scroll'](event.pos, event.delta[1])
    canvas.connect(on_mouse_wheel)

    def on_key_press(event):
        BINDINGS['key_press'](event.text)
        HELD_KEYS.append(event.text)
    canvas.connect(on_key_press)

    def on_key_release(event):
        HELD_KEYS.remove(event.text)
    canvas.connect(on_key_release)

    # Run
    timer.start()
    canvas.show()
    app.run()
