#version 130

in vec3 pos;
in vec3 norm;
in vec2 uv;

out vec3 vert_col;
out vec2 vert_uv;

uniform vec3 col;
uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

void main()
{
	gl_Position = proj * view * model * vec4(pos, 1.0f);
	vec3 world_norm = (model * vec4(norm, 0.0)).xyz;
	vec3 world_light = vec3(0.7,0.7,0.7);
	float calc = dot(world_norm, world_light);
	float light = clamp(calc, 0.0, 0.8)+0.2;

	vert_col = col * light;
	vert_uv = uv;
}
