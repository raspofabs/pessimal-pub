#version 130

in vec3 pos;
in vec2 uv;

out vec3 vert_col;
out vec2 vert_uv;

uniform vec3 col;
uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

void main()
{
	vec3 vertex_position = pos.xyz;
	gl_Position = proj * view * model * vec4(vertex_position, 1.0f);

	vert_col = col;
	vert_uv = uv;
}
