#version 430 core

in vec3 in_vertex;
in vec2 in_uv;
in mat4 in_model;
in vec3 in_normal;
in int in_tex_id;

uniform mat4 m_projection;
uniform mat4 m_view;

out vec2 tex_coords;
out vec3 normal;
out vec3 fragPosition;
out vec3 player;
flat out int tex_id;

void main() {
    tex_coords = in_uv;
    tex_id = in_tex_id;
    normal = mat3(transpose(inverse(in_model))) * in_normal;

    fragPosition = vec3(in_model * vec4(in_vertex, 1.0));
    gl_Position = m_projection * m_view * in_model * vec4(in_vertex, 1.0);
}