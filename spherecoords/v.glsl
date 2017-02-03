#version 120

// Using spherical coordinates.
attribute float rad;
attribute float azi;
attribute float inc;

vec4 spherical(float rad, float azi, float inc) {
    return vec4(rad*sin(inc)*cos(azi), rad*sin(inc)*sin(azi), rad*cos(inc), 1.0);
}

void main(void) {
    gl_Position = spherical(rad, azi, inc);
    gl_PointSize = 10.0;
}
