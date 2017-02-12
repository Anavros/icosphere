#version 120

uniform sampler2D slate;

void main(void) {
    gl_FragColor = texture2D(slate, gl_TexCoord[0].st);
}
