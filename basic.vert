#version 330

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

smooth out vec4 interp_color;

uniform vec3 dir_to_light;
uniform vec4 light_intensity;

uniform mat4 projection_matrix;
uniform mat4 modelview_matrix;

void main()
{
   gl_Position = projection_matrix * (modelview_matrix * vec4(position, 1.0));
   vec3 normCamSpace = normalize(modelview_matrix * vec4(normal, 0.0)).xyz;
   float cosAngIncidence = dot(normCamSpace, dir_to_light);
   cosAngIncidence = clamp(cosAngIncidence, 0, 1);
   interp_color = light_intensity * cosAngIncidence;
}
