#version 440 core

in vec3 in_vertex;
in vec3 in_color;
in mat4 in_model;

out vec3 axis_color;

uniform mat4 m_projection;
uniform mat4 m_view;

void main() {
    axis_color = in_color;
    gl_Position = m_projection * m_view * in_model * vec4(in_vertex, 1.0);
}
