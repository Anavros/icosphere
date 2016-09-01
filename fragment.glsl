#version 120

varying vec3 v_coloring;
uniform vec3 u_color;

void main(void) {
    //gl_FragColor = vec4(u_color, 1.0);
    gl_FragColor = vec4(v_coloring*u_color, 1);
}
