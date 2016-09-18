
from vispy import app, io, gloo
from vispy.gloo import gl
app.use_app('glfw')

SCREEN_W = 500
SCREEN_H = 500
SCALE = 1
CLEAR_COLOR = (1, 1, 1, 1)

CANVAS = None
CALLBACKS = {
    'draw': None,
    'update': None,
    'left_click': None,
    'right_click': None,
    'middle_click': None,
    'left_drag': None,
    'right_drag': None,
    'middle_drag': None,
    'scroll': None,
    'hover': None,
    'key_press': None,
    'key_hold': None,
}

def prep(size=(500, 500), title="Rocket Canvas", scale=1, clear_color=(1, 1, 1, 1)):
    global CANVAS, SCREEN_W, SCREEN_H, SCALE, CLEAR_COLOR
    SCREEN_W = size[0]
    SCREEN_H = size[1]
    SCALE = scale
    CANVAS = app.Canvas(
        size=size,
        title=title,
        keys='interactive',
        resizable=False,
        px_scale=scale,
    )
    CLEAR_COLOR = clear_color

# i.e. @rocket.attach
def attach(f):
    """
    Register a function to be called on a certain event.

    The event type is inferred from the function's name. Raises ValueError if
    the name of the function does not match any known event type.
    """
    name = f.__name__
    if name in CALLBACKS.keys():
        CALLBACKS[name] = f
    else:
        raise ValueError("unknown event @rocket.call: {}.".format(name))


def call(event_name, *args, **kwargs):
    #print(event_name)
    if CALLBACKS[event_name] is not None:
        CALLBACKS[event_name](*args, **kwargs)


def screen_to_world(coords):
    (x, y) = coords
    a = ((x/SCREEN_W)*2)-1
    b = -(((y/SCREEN_H)*2)-1)
    return (a, b)


def world_to_screen(coords):
    (a, b) = coords
    x = ((a+1)/2) * SCREEN_W
    y = ((-b+1)/2) * SCREEN_H
    return (x, y)


def launch(fps=None, autoclear=True, enablealpha=True):
    global CANVAS
    if not CANVAS:
        print("Warning: call rocket.prep() before launching. Setting default params.")
        prep()

    # Initialization
    # Enables transparency and depth buffering.
    if enablealpha:
        gl.glEnable(gl.GL_BLEND)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gloo.set_state(clear_color=CLEAR_COLOR, depth_test=True)
    else:
        gloo.set_state(clear_color=CLEAR_COLOR)

    timer = app.Timer(interval=('auto' if not fps else 1/fps))
    held_keys = []

    # Event Handling Functions
    def on_draw(event):
        if autoclear: gloo.clear(color=True, depth=True)
        call('draw')
    CANVAS.connect(on_draw)

    def on_update(event):
        if held_keys:
            call('key_hold', held_keys)
        call('update')
        CANVAS.update()
    timer.connect(on_update)

    def on_mouse_press(event):
        pass
    CANVAS.connect(on_mouse_press)

    def on_mouse_release(event):
        trail = event.trail()
        if trail is None or len(trail) <= 1:
            if event.button == 1:
                call('left_click', event.pos)
            elif event.button == 2:
                call('right_click', event.pos)
            elif event.button == 3:
                call('middle_click', event.pos)
        else:
            pass
    CANVAS.connect(on_mouse_release)

    def on_mouse_double_click(event):
        if event.last_event.button == 1:
            call('left_click', event.last_event.pos)
        elif event.last_event.button == 2:
            call('right_click', event.last_event.pos)
        elif event.last_event.button == 3:
            call('middle_click', event.last_event.pos)
    CANVAS.connect(on_mouse_double_click)

    def on_mouse_move(event):
        if event.button is None:
            call('hover', event.pos)
        else:
            (ax, ay) = event.last_event.pos
            (bx, by) = event.pos
            (dx, dy) = (bx - ax), (by - ay)
            if event.button == 1:
                call('left_drag', (ax, ay), (bx, by), (dx, dy))
            elif event.button == 2:
                call('right_drag', (ax, ay), (bx, by), (dx, dy))
            elif event.button == 3:
                call('middle_drag', (ax, ay), (bx, by), (dx, dy))
    CANVAS.connect(on_mouse_move)

    def on_mouse_wheel(event):
        call('scroll', event.pos, event.delta[1])
    CANVAS.connect(on_mouse_wheel)

    def on_key_press(event):
        call('key_press', event.text)
        held_keys.append(event.text)
    CANVAS.connect(on_key_press)

    def on_key_release(event):
        held_keys.remove(event.text)
    CANVAS.connect(on_key_release)

    # Run
    timer.start()
    CANVAS.show()
    app.run()
