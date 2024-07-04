import pygame
import sys
import os
import i18n
from OpenGL.GL import *
from enum import Enum
from pessimal.v2 import V2
from pessimal.camera import Camera2D
from .config import load_config, calculate_tuple
from .opengl_helper import OpenGLHelper
from .texture import Texture
from .model import ModelSprite
from .instance import Instance
from .shader import Shader, ShaderManager
import random

from .imgui_support import PygameRenderer
import imgui


class SystemStatus(Enum):
    EDITING = 1
    RUNNING = 2
    PAUSED = 3

FG_TEXT = (255, 255, 255)


class EngineDependent:
    """Base class for dependents on engine callbacks"""

    def __init__(self, engine):
        self.engine = engine
        engine.add_dependent(self)
        pass

    def handle_event(self, event):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def update(self, delta_time: float):
        pass

    def render(self, engine):
        pass


class Engine:
    def __init__(self):
        self.status = SystemStatus.RUNNING
        
        config = load_config()
        # setup localisation
        locale = "en"
        i18n.load_path.append("data/i18n")
        i18n.set('file_format', 'json')
        i18n.set('filename_format', '{namespace}.{format}')
        i18n.set('locale',locale)  # set again later in UIManager
        assert i18n.t("ui.play") == "Play", f"{i18n.t('ui.play') =}"
        pygame.init()

        # setup rendering
    
        infoObject = pygame.display.Info()
        w, h = infoObject.current_w, infoObject.current_h

        self.display_size = calculate_tuple(config, w, h, "screen_size", "50%, 50%")
        self.display_pos = calculate_tuple(config, w, h, "screen_pos", "25%, 25%")
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % self.display_pos
        self.opengl_helper = OpenGLHelper()
        self.screen_3d = self.opengl_helper.init_gl(self.display_size)
        ShaderManager.load_config("data/shaders/config.yaml")
        self.margin = 10
        self.screen_2d = pygame.Surface((self.display_size[0] - self.margin*2, self.display_size[1] - self.margin*2 - 20))

        print(f"screen {self.display_size}@{self.display_pos}")
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(f"pessimal {self.status}")
        self.display_centre = tuple(map(lambda x: x/2, self.display_size))
        self.font = pygame.font.SysFont("consolas", 16)
        self.camera = Camera2D(display_size=V2(*self.display_size))
        self.camera.centre_on(V2(0,0))

        self.dependents = []

        # setup 2d transfer objects
        self.transfer_texture = Texture.from_surface(self.screen_2d)
        self.transfer_model = ModelSprite()
        self.transfer_instance = Instance()
        shader = ShaderManager.get_shader("textured")
        self.transfer_instance.set_shader(shader)
        self.transfer_instance.set_model(self.transfer_model)
        self.transfer_instance.set_transform_pos([0.0, 0.0, 0.0])
        self.transfer_instance.transform[0] = self.display_size[0]
        self.transfer_instance.transform[5] = self.display_size[1]
        self.transfer_instance.set_colour([1.0, 1.0, 1.0])
        self.transfer_instance.set_texture(self.transfer_texture, 0)

        # imgui
        imgui.create_context()
        self.imgui_impl = PygameRenderer()

        self.imgui_io = imgui.get_io()
        font_file_path = "data/font/FantasqueSansMNerdFont-Regular.ttf"
        bold_font_file_path = "data/font/FantasqueSansMNerdFont-Bold.ttf"
        font_pixel_size = int(config.get("font_size", 24))
        self.imgui_font = self.imgui_io.fonts.add_font_from_file_ttf(
                font_file_path, font_pixel_size
                )
        self.imgui_bold_font = self.imgui_io.fonts.add_font_from_file_ttf(
                bold_font_file_path, font_pixel_size
                )
        self.imgui_impl.refresh_font_texture()
        self.imgui_io.display_size = self.display_size
        self.should_show_demo = False
        
        # lets go
        self.running = True

    def shutdown(self):
        sys.exit()

    def switch_status(self, new_status: SystemStatus):
        if self.status != new_status:
            if new_status == SystemStatus.EDITING:
                for dependent in self.dependents:
                    dependent.stop()
            if self.status == SystemStatus.EDITING:
                for dependent in self.dependents:
                    dependent.start()
            self.status = new_status
            pygame.display.set_caption(f"pessimal : {self.status}")

    def push_font_bold(self):
        imgui.push_font(self.imgui_bold_font)

    def list_fonts(self):
        fonts = pygame.font.get_fonts()
        print(len(fonts))
        for f in fonts:
            print(f)

    def get_window_pos(self):
        return pygame.display.get_window_position()

    def get_dt(self):
        return self.clock.get_time() / 1000.0

    def add_dependent(self, dependent):
        self.dependents.append(dependent)

    def tick(self):
        dt = self.get_dt()
        events = pygame.event.get()

        for event in events:
            #print(f"E: {event}")
            if event.type == pygame.QUIT:
                self.running = False
            for dependent in self.dependents:
                dependent.process_event(event)

            # ui processing
            self.imgui_impl.process_event(event)

        self.imgui_impl.process_inputs()
        imgui.new_frame()
        imgui.push_font(self.imgui_font)

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                        "Quit", "Cmd+Q", False, True
                        )

                if clicked_quit:
                    sys.exit(0)

                imgui.end_menu()
            if imgui.begin_menu("Help", True):
                clicked_show_demo, selected_show_demo = imgui.menu_item(
                        "Show Demo", None, self.should_show_demo, True
                        )

                if clicked_show_demo:
                    self.should_show_demo = not self.should_show_demo

                imgui.end_menu()
            #if imgui.button("menu button"):
            #    print("Menu button!")
            imgui.end_main_menu_bar()

        if self.should_show_demo:
            imgui.show_test_window()


        for dependent in self.dependents:
            dependent.update(dt)
            dependent.render(self)


        imgui.pop_font()
        self.end_frame()

    def clear_screen(self, colour):
        r, g, b, *a = colour
        # map 0-255 -> 0-1.0
        glClearColor(r/255.0, g/255.0, b/255.0, 1.0)
        glClearColor(0.5, 0.5, 0.5, 1.0)
        glClearDepth(1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.screen_2d.fill(colour)

    def end_frame(self):
        self.clock.tick(30)

        self.transfer_texture.update_texture_from_surface(self.screen_2d)
        Shader.set_aspect(self.display_size)
        Shader.set_ortho((0,0), self.display_size, -10, 100)
        self.transfer_instance.set_transform_pos([self.margin, self.margin + 20.0, 0.0])
        self.transfer_instance.transform[0] = self.display_size[0] - self.margin*2
        self.transfer_instance.transform[5] = self.display_size[1] - self.margin*2 - 20
        self.transfer_instance.render()
        imgui.render()
        self.imgui_impl.render(imgui.get_draw_data())
        pygame.display.flip()
    
    def should_render(self, pos: V2, size: float = 16.0):
        return True

    def render_sprite(self, sprite, pos: V2, size: V2 = V2(16,16)):
        screen_pos = self.camera.pos_to_screen(pos)
        screen_size = self.camera.size_to_screen(size)
        self.screen_2d.blit(pygame.transform.smoothscale(sprite, screen_size.as_coord()), screen_pos.as_coord())

    def render_circle(self, pos, size, colour):
        screen_pos = self.camera.pos_to_screen(pos)
        screen_size = self.camera.size_to_screen(size)
        screen_size_float = max(screen_size.as_coord())
        pygame.draw.circle(self.screen_2d, colour, screen_pos.as_coord(), screen_size_float)

    def render_rect(self, top_left, bottom_right, colour):
        screen_tl = self.camera.pos_to_screen(top_left)
        screen_br = self.camera.pos_to_screen(bottom_right) - screen_tl
        screen_rect = pygame.Rect(*screen_tl.as_coord(), *screen_br.as_coord())
        pygame.draw.rect(self.screen_2d, colour, screen_rect)

    def render_ui_rect(self, screen_rect, colour):
        pygame.draw.rect(self.screen_2d, colour, screen_rect)

    def render_line(self, start, end, colour):
        screen_start = self.camera.pos_to_screen(start)
        screen_end = self.camera.pos_to_screen(end)
        pygame.draw.line(self.screen_2d, colour, screen_start.as_coord(), screen_end.as_coord())

    def render_text(self, text, position):
        img = self.font.render(text, True, FG_TEXT)
        screen_pos = self.camera.pos_to_screen(position).as_coord()
        self.screen_2d.blit(img, screen_pos)

    def render_ui_text(self, text, position):
        img = self.font.render(text, True, FG_TEXT)
        self.screen_2d.blit(img, position)
