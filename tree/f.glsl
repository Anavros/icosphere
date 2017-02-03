#version 120

varying vec3 fr_c;

void main(void) {
    gl_FragColor = vec4(fr_c, 1);
}
