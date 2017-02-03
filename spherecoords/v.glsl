#version 120

// Using spherical coordinates.
attribute float rad;
attribute float ang;
attribute float phi;

vec4 spherical(float rad, float ang, float phi) {
    return vec4(rad*sin(phi)*cos(ang), rad*sin(phi)*sin(ang), rad*cos(phi), 1.0);
}

void main(void) {
    gl_Position = spherical(rad, ang, phi);
    gl_PointSize = 10.0;
}
