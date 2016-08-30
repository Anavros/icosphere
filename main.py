#!/usr/bin/env python3.4

"""
Generic Space Game

A hearty foray into game development.
"""

# Imports & Boilerplate
from vispy import app, gloo
from vispy.util.transforms import translate, scale, rotate
import numpy
app.use_app('glfw')

import game
import tools
from constants import SIZE, CLEAR_COLOR, TITLE


def main():
    # Important Variables
    canvas = app.Canvas(title=TITLE, size=SIZE, keys='interactive')
    program = tools.build_program("vertex.glsl", "fragment.glsl")
    program['a_position'] = gloo.VertexBuffer(tools.square())
    timer = app.Timer()
    held_keys = []

    # Event Handling Functions
    def on_draw(event):
        gloo.clear(CLEAR_COLOR)
        game.draw(program)
    canvas.connect(on_draw)

    def on_update(event):
        if held_keys:
            game.key_hold(held_keys)
        game.update(event)
        canvas.update()
    timer.connect(on_update)

    def on_mouse_press(event):
        pass
    canvas.connect(on_mouse_press)

    def on_mouse_release(event):
        trail = event.trail()
        if trail is None or len(trail) <= 1:
            if event.button == 1:
                game.left_click(event.pos)
            elif event.button == 2:
                game.right_click(event.pos)
            elif event.button == 3:
                game.middle_click(event.pos)
        else:
            pass
    canvas.connect(on_mouse_release)

    def on_mouse_double_click(event):
        if event.last_event.button == 1:
            game.left_click(event.pos)
        elif event.last_event.button == 2:
            game.right_click(event.pos)
        elif event.last_event.button == 3:
            game.middle_click(event.pos)
    canvas.connect(on_mouse_double_click)

    def on_mouse_move(event):
        if event.button is None:
            game.hover(tools.screen_to_world(event.pos))
        else:
            (a1, b1) = tools.screen_to_world(event.last_event.pos)
            (a2, b2) = tools.screen_to_world(event.pos)
            (da, db) = (a2-a1, b2-b1)
            if event.button == 1:
                game.left_click_and_drag((a1, b1), (a2, b2), (da, db))
            elif event.button == 2:
                game.right_click_and_drag((a1, b1), (a2, b2), (da, db))
            elif event.button == 3:
                game.middle_click_and_drag((a1, b1), (a2, b2), (da, db))
    canvas.connect(on_mouse_move)

    def on_mouse_wheel(event):
        game.scroll(event.pos, event.delta[1])
    canvas.connect(on_mouse_wheel)

    def on_key_press(event):
        game.key_press(event.text)
        held_keys.append(event.text)
    canvas.connect(on_key_press)

    def on_key_release(event):
        held_keys.remove(event.text)
    canvas.connect(on_key_release)

    # Run
    timer.start()
    canvas.show()
    app.run()


if __name__ == '__main__':
    main()
