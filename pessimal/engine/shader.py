# pragma: exclude file
# shader requires OpenGL

import math
import numpy as np
import os
from .opengl_helper import check_gl_error
from .math_support import *
from OpenGL.GL import *
import yaml


class Shader:
    x_camera_pos = 0
    y_camera_pos = 0
    z_camera_pos = 0
    y_camera_angle = 0
    view_matrix = m44_get_identity()
    camera_matrix = m44_get_identity()
    aspect = 16/9

    def __init__(self, vertex: 'os.PathLike[str]', fragment: 'os.PathLike[str]'):
        vert = source_shader(vertex, GL_VERTEX_SHADER)
        frag = source_shader(fragment, GL_FRAGMENT_SHADER)
        self.program = link_shader(vert, frag)
        glDeleteShader(vert)
        glDeleteShader(frag)

        self.l_pos = glGetAttribLocation(self.program, "pos")
        self.l_uv = glGetAttribLocation(self.program, "uv")
        self.l_norm = glGetAttribLocation(self.program, "norm")
        self.l_instance_pos = glGetAttribLocation(self.program, "instance_pos")

        self.l_col = glGetUniformLocation(self.program, "col")

        self.l_samplers = [glGetUniformLocation(self.program, "sampler_1")]

        self.l_model = glGetUniformLocation(self.program, "model")
        self.l_view = glGetUniformLocation(self.program, "view")
        self.l_proj = glGetUniformLocation(self.program, "proj")
        self.fov = math.pi / 4
        self.z_far = 10000.0
        self.z_near = 0.1
        self.projection_matrix = None
        Shader.x_camera_pos, Shader.y_camera_pos, Shader.z_camera_pos = 0.0, 0.0, 10.0

    def set_texture(self, slot, texture):
        glUseProgram(self.program)
        if self.l_samplers[slot] != 0:
            glActiveTexture(GL_TEXTURE0 + slot)
            glBindTexture(GL_TEXTURE_2D, texture.id)
            glUniform1i(self.l_samplers[slot], slot)

    @classmethod
    def set_aspect(cls, aspect):
        if type(aspect) == tuple:
            Shader.aspect = aspect[0]/aspect[1]
        else:
            Shader.aspect = aspect
        Shader.projection_matrix = None

    @classmethod
    def set_cam_yx(cls, pos, yaw, pitch):
        cls.projection = "perspective"
        Shader.y_camera_angle = yaw
        x_mat = as44(m44_get_x_rot(pitch))
        y_mat = as44(m44_get_y_rot(yaw))
        translation = as44(m44_get_translation(*pos))
        rotation = np.matmul(x_mat, y_mat)
        orientation = np.matmul(rotation, translation)
        Shader.camera_matrix = as_list(orientation)
        cam_view = np.linalg.inv(orientation)
        Shader.view_matrix = as_list(cam_view)

    @classmethod
    def set_ortho(cls, top_left, bottom_right, near, far):
        cls.projection = "orthogonal"
        cls.top = top_left[1]
        cls.left = top_left[0]
        cls.bottom = bottom_right[1]
        cls.right = bottom_right[0]
        cls.near = near
        cls.far = far
        Shader.view_matrix = m44_get_identity()
        Shader.view_matrix[0] = -1

    @classmethod
    def set_look_at(cls, pos, focus):
        cls.projection = "perspective"
        up_base = [0.0, 1.0, 0.0]
        fwd = v_normalize(np.subtract(focus, pos))
        side = v_normalize(np.cross(fwd, up_base))
        up = np.cross(side, fwd)
        Shader.view_matrix = [
            side[0], up[0], -fwd[0], 0,
            side[1], up[1], -fwd[1], 0,
            side[2], up[2], -fwd[2], 0,
            np.dot(side, pos), np.dot(up, pos), np.dot(fwd, pos), 1.0
        ]
        #print(Shader.view_matrix)

    @classmethod
    def get_camera_forward(cls):
        return Shader.camera_matrix[8:12]

    @classmethod
    def get_camera_left(cls):
        return Shader.camera_matrix[0:4]

    @classmethod
    def get_camera_up(cls):
        return Shader.camera_matrix[4:8]

    @classmethod
    def get_view_matrix(cls):
        return Shader.view_matrix

    @classmethod
    def set_view_y(cls, y):
        Shader.y_camera_angle = y
        Shader.view_matrix = [
            np.cos(y), 0.0, -np.sin(y), 0.0,
            0.0, 1.0, 0.0, 0.0,
            np.sin(y), 0.0, np.cos(y), 0.0,
            Shader.x_camera_pos, Shader.y_camera_pos, Shader.z_camera_pos, 1.0]

    @classmethod
    def set_view_pos(cls, pos):
        Shader.x_camera_pos, Shader.y_camera_pos, Shader.z_camera_pos = pos
        Shader.view_matrix = Shader.view_matrix[:12]+pos+[1.0]

    def get_orthographic(self):
        self.projection_matrix = [
            2.0 / (self.left-self.right), 0.0, 0.0, 0.0,
            0.0, 2.0 / (self.top-self.bottom), 0.0, 0.0,
            0.0, 0.0, -2.0 / (self.far-self.near), 0.0,

            -(self.left + self.right) / (self.right - self.left),
            -(self.top + self.bottom) / (self.top - self.bottom),
            -(self.far + self.near) / (self.far - self.near),
            1.0,
            ]
        return self.projection_matrix

    def get_perspective(self):
        if self.projection_matrix is None:
            y_max = self.z_near * np.tan(self.fov/2)
            x_max = y_max * Shader.aspect
            div = 1.0 / (self.z_far - self.z_near)
            self.projection_matrix = [
                self.z_near / x_max, 0.0, 0.0, 0.0,
                0.0, self.z_near / y_max, 0.0, 0.0,
                0.0, 0.0, -(self.z_far+self.z_near) * div, -1.0,
                0.0, 0.0, -2.0 * self.z_far * self.z_near * div, 0.0
            ]
        return self.projection_matrix

    def get_projection(self):
        if self.projection == "orthogonal":
            return self.get_orthographic()
        elif self.projection == "perspective":
            return self.get_perspective()
        else:
            return m44_get_identity()

    def draw_model(self, model, model_matrix=None, col=None, instance_pos_vbo=None, num_instances=0):
        if model_matrix is None:
            model_matrix = m44_get_identity()
        glUseProgram(self.program)
        check_gl_error()
        glUniformMatrix4fv(self.l_proj, 1, False, self.get_projection())
        glUniformMatrix4fv(self.l_view, 1, False, self.get_view_matrix())
        glUniformMatrix4fv(self.l_model, 1, False, model_matrix)
        if col is not None:
            glUniform3f(self.l_col, *col)
        else:
            glUniform3f(self.l_col, 1.0, 1.0, 1.0)
        check_gl_error()

        glEnableVertexAttribArray(self.l_pos)
        glBindBuffer(GL_ARRAY_BUFFER, model.pos_vbo)
        glVertexAttribPointer(self.l_pos, 3, GL_HALF_FLOAT, False, 0, None)
        glVertexAttribDivisor(self.l_pos, 0)
        check_gl_error()
        draw_instances = False
        if self.l_norm != -1:
            glEnableVertexAttribArray(self.l_norm)
            glBindBuffer(GL_ARRAY_BUFFER, model.norm_vbo)
            glVertexAttribPointer(self.l_norm, 3, GL_HALF_FLOAT, False, 0, None)
            glVertexAttribDivisor(self.l_norm, 0)
            check_gl_error()
        if self.l_instance_pos != -1 and instance_pos_vbo is not None:
            glEnableVertexAttribArray(self.l_instance_pos)
            draw_instances = True
            glBindBuffer(GL_ARRAY_BUFFER, instance_pos_vbo)
            glVertexAttribPointer(self.l_instance_pos, 3, GL_HALF_FLOAT, False, 0, None)
            glVertexAttribDivisor(self.l_instance_pos, 1)
            check_gl_error()
        if self.l_uv != -1:
            glEnableVertexAttribArray(self.l_uv)
            glBindBuffer(GL_ARRAY_BUFFER, model.uv_vbo)
            glVertexAttribPointer(self.l_uv, 2, GL_HALF_FLOAT, False, 0, None)
            glVertexAttribDivisor(self.l_uv, 0)
            check_gl_error()

        glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        if draw_instances:
            glDrawArraysInstanced(GL_TRIANGLES, 0, 3*model.tri_count, num_instances)
        else:
            glDrawArrays(GL_TRIANGLES, 0, 3*model.tri_count)
        check_gl_error()


class ShaderManager:
    shader_info = {}
    shader_folder = ""

    @classmethod
    def load_config(cls, filepath):
        cls.shader_folder = os.path.dirname(filepath)
        with open(filepath) as yaml_file:
            shader_data = yaml.safe_load(yaml_file)
        # print(f"Shader info: {json.dumps(shader_data, indent=2)}")
        shader_list = shader_data.get("shaders", None)
        if shader_list:
            for shader_config in shader_list:
                cls.shader_info[shader_config["name"]] = shader_config

    @classmethod
    def get_shader(cls, name) -> Shader:
        if name in cls.shader_info:
            info = cls.shader_info[name]
            if "shader" not in info:
                vert_filename = os.path.join(cls.shader_folder, info["vert"])
                frag_filename = os.path.join(cls.shader_folder, info["frag"])
                info["shader"] = Shader(vert_filename, frag_filename)
            return info["shader"]
        else:
            return None




def link_shader(vertex_shader, fragment_shader):
    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    glDetachShader(program, vertex_shader)
    glDetachShader(program, fragment_shader)
    success = glGetProgramiv(program, GL_LINK_STATUS)
    if not success:
        print(f"shader linking failed.\n{glGetProgramInfoLog(program)}")
    return program


def source_shader(filename: 'os.PathLike[str]', shader_type: 'os.PathLike[str]'):
    source = open(filename, "rt").read()
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    success = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not success:
        print(f"shader compilation failed for {filename}:\n{glGetShaderInfoLog(shader)}")
    return shader

