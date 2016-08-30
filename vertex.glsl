#version 120

attribute vec3 a_position;
attribute vec3 a_coloring;
uniform mat4 m_view;
uniform mat4 m_model;
varying vec3 v_coloring;

void main(void) {
    gl_Position = m_view * m_model * vec4(a_position, 1.0);
    gl_PointSize = 10.0;
    v_coloring = a_coloring;
}
