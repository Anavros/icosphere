#version 120

attribute vec2 pos;
attribute vec2 tex;

void main(void) {
    gl_Position = vec4(pos.xy, 0, 1);
    gl_TexCoord[0] = vec4(tex, 0, 1);
}
