from functools import lru_cache
from ast import literal_eval


class Component:
    # components should write their own field data
    fields = []

    def __init__(self, parent, config: dict = None):
        self.parent = parent
        if config is not None:
            for field in self.fields:
                field.read(self, config)

    def get_world(self):
        assert self.parent is not None
        return self.parent.get_world()

    def save_out(self):
        config = {"type": self.__class__.__name__}
        for field in self.fields:
            config[field.name] = field.store(self)
        return config

    @staticmethod
    def get_all_component_types():
        subclasses = set()
        work = [Component]
        while work:
            current_class = work.pop()
            for child in current_class.__subclasses__():
                if child not in subclasses:
                    subclasses.add(child)
                    work.append(child)
        return list(subclasses)

    @lru_cache
    @staticmethod
    def get_class_from_name(name):
        subclasses = set()
        work = [Component]
        while work:
            current_class = work.pop()
            for child in current_class.__subclasses__():
                if child not in subclasses:
                    if child.__name__ == name:
                        return child
                    subclasses.add(child)
                    work.append(child)
        return None

    @classmethod
    def create(cls, config, parent):
        name = config.get("type")
        if name is None:
            return None

        constructor = cls.get_class_from_name(name)
        if constructor is not None:
            return constructor(parent, config)
        return None

    def start(self):
        pass

    def stop(self):
        pass

    def update(self, dt):
        pass

    def render(self, engine):
        pass

