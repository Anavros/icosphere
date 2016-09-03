#!/usr/bin/env python3.4

import rocket

def main():
    canvas = tools.make_canvas((0, 0), title='')
    shader = tools.make_shader('shader.glsl', 'fragment.glsl')
    rocket.launch(canvas)


@rocket.call
def draw(program):
    pass


@rocket.call
def update():
    pass


if __name__ == '__main__':
    main()
