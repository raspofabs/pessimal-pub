# pragma: exclude file
# this simple file interacts deeply with OpenGL, making testing difficult.

from OpenGL.GL import *
import pygame
import os
from imgui.integrations.opengl import get_common_gl_state, restore_common_gl_state


def check_gl_error():
    status = glGetError()
    if status != GL_NO_ERROR:
        raise RuntimeError("gl error %s" % (status,))


class OpenGLHelper:
    def __init__(self):
        self.state = None

    def init_gl(self, window_size):
        assert os.environ.get("SDL_VIDEODRIVER") != "dummy"
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 1)
        self.screen = pygame.display.set_mode(
            window_size, pygame.DOUBLEBUF | pygame.OPENGL
        )
        glDepthMask(GL_TRUE)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glFrontFace(GL_CCW)
        glShadeModel(GL_SMOOTH)
        glDepthRange(0.0, 1.0)
        return self.screen

    def stash_state(self):
        assert self.state is None
        global imgui_restore_point
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        common_gl_state_tuple = get_common_gl_state()
        last_program = glGetIntegerv(GL_CURRENT_PROGRAM)
        last_active_texture = glGetIntegerv(GL_ACTIVE_TEXTURE)
        last_array_buffer = glGetIntegerv(GL_ARRAY_BUFFER_BINDING)
        last_element_array_buffer = glGetIntegerv(GL_ELEMENT_ARRAY_BUFFER_BINDING)
        last_vertex_array = glGetIntegerv(GL_VERTEX_ARRAY_BINDING)
        self.state = (
            common_gl_state_tuple,
            last_program,
            last_active_texture,
            last_array_buffer,
            last_element_array_buffer,
            last_vertex_array,
        )

    def reload_state(self):
        assert self.state is not None
        (
            common_gl_state_tuple,
            last_program,
            last_active_texture,
            last_array_buffer,
            last_element_array_buffer,
            last_vertex_array,
        ) = self.state
        restore_common_gl_state(common_gl_state_tuple)
        glUseProgram(last_program)
        glActiveTexture(last_active_texture)
        glBindVertexArray(last_vertex_array)
        glBindBuffer(GL_ARRAY_BUFFER, last_array_buffer)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, last_element_array_buffer)
        self.state = None
