from functools import lru_cache
from pessimal.v2 import V2
from ast import literal_eval
import json


class Field:
    def __init__(self, name: str, default_value):
        self.name = name
        self.default_value = default_value

    def read(self, destination, config):
        string_value = config.get(self.name)
        if string_value in [None, "None"]:
            value = self.default_value
        else:
            try:
                value = self.parse(string_value)
            except:
                print(f"Error when parsing {self.name} : {self.__class__.__name__}/{self.default_value}")
                print(f"Field string : >>{string_value}<<")
                raise
        setattr(destination, self.name, value)

    def get_value(self, source):
        return getattr(source, self.name)

    def set_value(self, destination, new_value):
        return setattr(destination, self.name, new_value)

    def store(self, source):
        return self.serialise(getattr(source, self.name))
    
    def parse(self, value):
        return value

    def serialise(self, value):
        return str(value)


class IntField(Field):
    def parse(self, value):
        return int(value)

    def serialise(self, value):
        return value

class FloatField(Field):
    def parse(self, value):
        return float(value)

    def serialise(self, value):
        return value

class DictField(Field):
    def parse(self, value):
        if not isinstance(value, dict):
            return json.loads(value)
        return value
    
    def serialise(self, value):
        return value

class ListField(Field):
    def parse(self, value):
        if not isinstance(value, list):
            return literal_eval(value)
        return value
    
    def serialise(self, value):
        return value

class V2Field(Field):
    def parse(self, value):
        return V2.parse(value)


class LiteralField(Field):
    def parse(self, value):
        return literal_eval(value)


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

