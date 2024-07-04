#version 130

in vec3 vert_col;
in vec2 vert_uv;

out vec4 out_rgba;

uniform sampler2D sampler_1;

void main()
{
	out_rgba = vec4(vert_col,1.0);
	//vec2 fragmentScreenCoordinates = vec2(gl_FragCoord.x / _ScreenParams.x, gl_FragCoord.y / _ScreenParams.y);
	out_rgba.x = mod(gl_FragCoord.x/256.0,1.0);
	out_rgba.y = mod(gl_FragCoord.y/256.0,1.0);
	out_rgba.xyz = vec3(mod(gl_FragCoord.z/0.01,1.0));
	out_rgba.y = mod(gl_FragCoord.w/0.01,1.0);
	out_rgba.xyz = texture2D(sampler_1, mod(gl_FragCoord.xy/32.0,1.0)).xyz;
	out_rgba.xyz = texture2D(sampler_1, vert_uv).xyz * vert_col;

}
