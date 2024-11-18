#version 430

layout (location=0) out vec4 fragColor;

//struct Material {
//
//};


uniform sampler2D diffuse_tex;
uniform sampler2D metallic_tex;
uniform sampler2D roughness_tex;

void main() {
    fragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
