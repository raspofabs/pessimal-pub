from OpenGL.GL import *
import pygame

class Texture:
    def __init__(self, size, data):
        self.id = glGenTextures(1)
        self.data = data
        self.size = size
        width, height = size

        glBindTexture(GL_TEXTURE_2D, self.id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.data)
        glGenerateTextureMipmap(self.id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    @staticmethod
    def from_surface(surface):
        data = pygame.image.tostring(surface, "RGBA", False)
        return Texture(surface.size, data)

    def update_texture_from_surface(self, surface):
        new_data = pygame.image.tostring(surface, "RGBA", False)
        width, height = self.size
        glBindTexture(GL_TEXTURE_2D, self.id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, new_data)
        glGenerateTextureMipmap(self.id)


    def read(self, filename: 'os.PathLike[str]'):
        self.image = pygame.image.load(filename)
        # print(f"Image {filename} -> {self.image.get_width()} x {self.image.get_height()}")
        self.data = pygame.image.tostring(self.image, "RGBA", False)
        width = self.image.get_width()
        height = self.image.get_height()
        glBindTexture(GL_TEXTURE_2D, self.id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.data)
        glGenerateTextureMipmap(self.id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    def read_xml(self, filename: 'os.PathLike[bytes]', print_names=False):
        xml_data = xmltodict.parse(open(filename).read())
        prepend = os.path.dirname(filename)
        atlas = xml_data["TextureAtlas"]
        image_filename = atlas["@imagePath"]
        image_path = os.path.join(prepend, image_filename)
        self.read(image_path)
        i_width = self.image.get_width()
        i_height = self.image.get_height()
        for sub_texture in atlas["SubTexture"]:
            x = int(sub_texture["@x"])
            y = int(sub_texture["@y"])
            w = int(sub_texture["@width"])
            h = int(sub_texture["@height"])
            x /= i_width
            y /= i_height
            w /= i_width
            h /= i_height
            name = sub_texture["@name"]
            if print_names:
                print(f"Sheet[{os.path.split(filename)[-1]}] : {name}")
            self.lookup[name] = (x, y, w, h)

    def get_uvs_for(self, sprite_name):
        if sprite_name in self.lookup:
            return self.lookup[sprite_name]
        return 0, 0, 1, 1

