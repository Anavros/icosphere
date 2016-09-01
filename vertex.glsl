#version 120

attribute vec3 a_position;
attribute vec3 a_coloring;
uniform mat4 m_view;
uniform mat4 m_model;
uniform mat4 m_proj;
varying vec3 v_coloring;
uniform vec3 u_color;

void main(void) {
    gl_Position = m_proj * m_view * m_model * vec4(a_position, 1.0);
    gl_PointSize = 2.5;
    v_coloring = a_coloring;
}
