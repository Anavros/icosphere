#version 120

attribute vec2 a_position;
uniform mat4 m_view;
uniform mat4 m_model;

void main(void) {
    gl_Position = m_view * m_model * vec4(a_position, 0.0, 1.0);
    gl_PointSize = 10.0;
}
