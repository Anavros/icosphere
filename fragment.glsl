#version 120

varying vec3 v_coloring;

vec4 gradient(void) {
    vec2 position = (gl_FragCoord.xy / vec2(480.0));

    vec4 top = vec4(1.0, 0.0, 1.0, 1.0);
    vec4 bottom = vec4(1.0, 1.0, 0.0, 1.0);

    return vec4(mix(bottom, top, position.y));
}

void main(void) {
    //gl_FragColor = vec4(0.5, 0.6, 0.9, 1);
    gl_FragColor = vec4(v_coloring, 1);
    //gl_FragColor = gradient();
}
