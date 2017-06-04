#version 120

attribute vec3 a_position;
attribute vec3 a_coloring;
uniform mat4 m_view;
uniform mat4 m_model;
uniform mat4 m_proj;
varying vec3 v_coloring;
uniform vec3 u_color;

/* Convert spherical coordinates to cartesian. */
/* Takes radius, azimuth, and inclination. */
vec4 spherical(float rad, float azi, float inc) {
    return vec4(rad*sin(inc)*cos(azi), rad*sin(inc)*sin(azi), rad*cos(inc), 1.0);
}

void main(void) {
    // For spherical coordinates.
    //gl_Position = (proj * view * modl * spherical(rad, azi, inc));

    // For cartesian coordinates.
    gl_Position = m_proj * m_view * m_model * vec4(a_position, 1.0);

    gl_PointSize = 2.5;
    v_coloring = a_coloring;
}
