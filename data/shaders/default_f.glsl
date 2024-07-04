#version 130

in vec3 vert_col;

out vec4 out_rgba;

void main()
{
	out_rgba = vec4(vert_col,1.0);
}
