#version 120

attribute vec2 pos;

void main(void) {
    gl_Position = vec4(pos, 0, 1);
    gl_PointSize = 10;
}
