#version 430 core

out vec4 fragColor;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

struct PointLight {
    vec3 PL_position;
    vec3 PL_color;
    float PL_specular;
    float PL_radius;
    int PL_intensity;
};

struct DirectionalLight {
    vec3 DL_direction;
    vec3 DL_position;
    float DL_radius;
    float DL_angle;
    float DL_dist;
    bool isSun;
};

in vec2 tex_coords;
in vec3 normal;
in vec3 fragPosition;
flat in int tex_id;

#define MAX_POINT_LIGHTS 16
#define MAX_DIR_LIGHTS 16
uniform PointLight point_lights[MAX_POINT_LIGHTS];
//uniform DirectionalLight directional_lights[MAX_DIR_LIGHTS];

uniform sampler2DArray texture_array;
uniform vec3 player_position;
uniform float u_time = 0;
uniform vec3 ambient_light = vec3(0.03, 0.03, 0.04);

vec3 getPointLight(PointLight light) {
    ////// Calculating all necessary vectors //////

    // Light direction vector
    vec3 light_dir = normalize(light.PL_position - fragPosition);
    // Current direction from player veiw pos to pixel
    vec3 view_dir = normalize(player_position - fragPosition);
    // Reflection vector for light
    vec3 reflect_dir = reflect(-light_dir, normal);


    /////// Calculating light intensity ///////

    // Checking how well the view vector matches the reflection vector
    float spec_ratio = pow(max(dot(view_dir, reflect_dir), 0.0), 32);
    // Find the specular intensity
    vec3 light_specular = light.PL_specular * spec_ratio * light.PL_color;
    // Find clamped dictance from pixel to light source
    float light_dist = clamp(length(light.PL_position - fragPosition), 0, light.PL_radius);
    float light_dist_ratio = light.PL_radius - light_dist;
    // Find the light diffuse light intensity multiplier
    float light_diff_ratio = clamp(dot(normal, light_dir), 0.f, 1.f)*light_dist_ratio;
    // Diffuse light total value
    vec3 light_diffuse = light_diff_ratio * light.PL_color * float(light.PL_intensity);


    // Light intensity total value for pixel
    vec3 result = (light_diffuse + light_specular);
    return result;
}

vec3 getDirectionalLight(DirectionalLight light, vec3 color) {
    vec3 result = vec3(0.f);
    return result;
}


void main() {
    vec3 diffuse_color = texture(texture_array, vec3(tex_coords, tex_id)).rgb;
//    vec3 diffuse_color = vec3(1.0);

    // Transform gamma for changing color
    diffuse_color = pow(diffuse_color, gamma);
    vec3 result_color = vec3(0.f);

//    for (uint i = 0; i < directional_lights.length(); i++) {
//        // Adding a value for each directional light source
//        result_color += getDirectionalLight(directional_lights[i], diffuse_color);
//    }

    for (uint i = 0; i < point_lights.length(); i++) {
        // Adding a value for each point light source
        result_color += getPointLight(point_lights[i]);
    }
    diffuse_color *= ambient_light + result_color;

    // FOG Calculations
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
    diffuse_color = mix(diffuse_color, ambient_light, (1.0 - exp2(-0.003 * fog_dist * fog_dist)));

    // Return to standard gamma value
    diffuse_color = pow(diffuse_color, inv_gamma);


    fragColor = vec4(diffuse_color, 1.0);
}