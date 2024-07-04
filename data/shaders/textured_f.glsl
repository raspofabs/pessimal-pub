#version 130

in vec3 vert_col;
in vec2 vert_uv;

out vec4 out_rgba;

uniform sampler2D sampler_1;

void main()
{
	out_rgba = vec4(texture2D(sampler_1, vert_uv).xyz * vert_col,1.0);

}
