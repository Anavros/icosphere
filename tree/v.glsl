#version 120

attribute vec2 pos;
attribute vec3 col;

varying vec3 fr_c;

void main(void) {
    gl_Position = vec4(pos, 0, 1);
    gl_PointSize = 5;
    fr_c = col;
}
