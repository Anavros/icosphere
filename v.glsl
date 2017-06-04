#version 120

// Using spherical coordinates.
attribute float rad;
attribute float azi;
attribute float inc;
attribute vec2 tex;
uniform mat4 modl;
uniform mat4 view;
uniform mat4 proj;

vec4 spherical(float rad, float azi, float inc) {
    return vec4(rad*sin(inc)*cos(azi), rad*sin(inc)*sin(azi), rad*cos(inc), 1.0);
}

void main(void) {
    gl_Position = (proj * view * modl * spherical(rad, azi, inc));
    gl_PointSize = 4.0;
    gl_TexCoord[0] = vec4(tex, 0, 1);
}
