#version 440 core

out vec4 fragColor;

in vec3 axis_color;

void main() {
    fragColor = vec4(axis_color, 1.0);
}
