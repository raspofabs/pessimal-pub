# pragma: exclude file
# model requires OpenGL

from OpenGL.GL import *
from .opengl_helper import check_gl_error
import numpy as np


class Model:
    def __init__(self):
        self.pos_vbo = glGenBuffers(1)
        self.norm_vbo = glGenBuffers(1)
        self.uv_vbo = glGenBuffers(1)
        self.tri_count = 0
        self.shader = None


class ModelSprite(Model):
    def __init__(self):
        super().__init__()
        face_vert_array = [
            0,
            0,
            0,
            0,
            1,
            0,
            1,
            0,
            0,
            1,
            0,
            0,
            0,
            1,
            0,
            1,
            1,
            0,
        ]
        face_vert_data = np.array(face_vert_array, dtype=np.float16)
        glBindBuffer(GL_ARRAY_BUFFER, self.pos_vbo)
        glBufferData(GL_ARRAY_BUFFER, face_vert_data, GL_STATIC_DRAW)
        check_gl_error()
        face_uv_array = [
            0,
            0,
            0,
            1,
            1,
            0,
            1,
            0,
            0,
            1,
            1,
            1,
        ]
        face_uv_data = np.array(face_uv_array, dtype=np.float16)
        glBindBuffer(GL_ARRAY_BUFFER, self.uv_vbo)
        glBufferData(GL_ARRAY_BUFFER, face_uv_data, GL_STATIC_DRAW)
        check_gl_error()
        face_norm_array = [0, 0, 1] * 6
        face_norm_data = np.array(face_norm_array, dtype=np.float16)
        glBindBuffer(GL_ARRAY_BUFFER, self.norm_vbo)
        glBufferData(GL_ARRAY_BUFFER, face_norm_data, GL_STATIC_DRAW)
        check_gl_error()
        self.tri_count = 2


class ModelCube(Model):
    def __init__(self):
        super().__init__()
        # lets start with a cube (6 faces of 3 verts each)
        cube_vert_array = [
            1,
            1,
            1,
            1,
            1,
            -1,
            -1,
            1,
            -1,
            1,
            1,
            1,
            -1,
            1,
            -1,
            -1,
            1,
            1,
            -1,
            1,
            1,
            -1,
            -1,
            1,
            1,
            -1,
            1,
            1,
            1,
            1,
            -1,
            1,
            1,
            1,
            -1,
            1,
            -1,
            -1,
            -1,
            -1,
            -1,
            1,
            -1,
            1,
            1,
            -1,
            -1,
            -1,
            -1,
            1,
            1,
            -1,
            1,
            -1,
            1,
            1,
            -1,
            -1,
            -1,
            -1,
            -1,
            1,
            -1,
            1,
            1,
            -1,
            1,
            -1,
            -1,
            -1,
            -1,
            -1,
            1,
            1,
            1,
            1,
            -1,
            -1,
            1,
            1,
            -1,
            1,
            -1,
            -1,
            1,
            1,
            1,
            1,
            -1,
            1,
            1,
            -1,
            1,
            -1,
            -1,
            -1,
            1,
            -1,
            -1,
            1,
            -1,
            1,
            -1,
            -1,
            1,
            -1,
            -1,
            -1,
        ]
        cube_vert_array = [x / 2 for x in cube_vert_array]
        cube_data = np.array(cube_vert_array, dtype=np.float16)
        glBindBuffer(GL_ARRAY_BUFFER, self.pos_vbo)
        glBufferData(GL_ARRAY_BUFFER, cube_data, GL_STATIC_DRAW)
        check_gl_error()
        cube_uv_array = [
            0,
            0,
            1,
            0,
            1,
            1,
            0,
            0,
            1,
            1,
            0,
            1,
            0,
            0,
            0,
            1,
            1,
            1,
            1,
            0,
            0,
            0,
            1,
            1,
            0,
            1,
            1,
            1,
            1,
            0,
            0,
            1,
            1,
            0,
            0,
            0,
            1,
            0,
            0,
            1,
            0,
            0,
            1,
            0,
            1,
            1,
            0,
            1,
            1,
            0,
            0,
            1,
            0,
            0,
            0,
            1,
            1,
            0,
            1,
            1,
            1,
            1,
            0,
            0,
            1,
            0,
            1,
            1,
            0,
            1,
            0,
            0,
        ]
        cube_data = np.array(cube_uv_array, dtype=np.float16)
        glBindBuffer(GL_ARRAY_BUFFER, self.uv_vbo)
        glBufferData(GL_ARRAY_BUFFER, cube_data, GL_STATIC_DRAW)
        check_gl_error()
        cube_norm_array = (
            [+0, 1, 0] * 6
            + [0, 0, 1] * 6
            + [-1, 0, 0] * 6
            + [0, 0, -1] * 6
            + [+1, 0, 0] * 6
            + [0, -1, 0] * 6
        )
        cube_data = np.array(cube_norm_array, dtype=np.float16)
        glBindBuffer(GL_ARRAY_BUFFER, self.norm_vbo)
        glBufferData(GL_ARRAY_BUFFER, cube_data, GL_STATIC_DRAW)
        check_gl_error()
        self.tri_count = 6
