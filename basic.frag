#version 330

smooth in vec4 interp_color;
smooth in vec2 texture_coordinate;

uniform sampler2D tex;

out vec4 outputColor;

void main()
{
   outputColor = interp_color * texture(tex, texture_coordinate);
}