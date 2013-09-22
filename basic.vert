#version 330

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec2 texcoord;

smooth out vec4 interp_color;
smooth out vec2 texture_coordinate;

uniform vec3 dir_to_light;
uniform vec4 light_intensity;
uniform vec4 ambient_intensity;

uniform mat4 projection_matrix;
uniform mat4 modelview_matrix;

void main()
{
   gl_Position = projection_matrix * (modelview_matrix * vec4(position, 1.0));
   vec3 normCamSpace = normalize(modelview_matrix * vec4(normal, 0.0)).xyz;
   float cosAngIncidence = dot(normCamSpace, dir_to_light);
   cosAngIncidence = clamp(cosAngIncidence, 0, 1);
   interp_color = light_intensity * cosAngIncidence + ambient_intensity;
   texture_coordinate = texcoord;
}
