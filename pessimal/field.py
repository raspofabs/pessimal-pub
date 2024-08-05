from pessimal.v2 import V2
from ast import literal_eval
import json
import imgui
import copy


class Field:
    def __init__(self, name: str, default_value, *, config: dict = None):
        self.name = name
        self.default_value = copy.deepcopy(default_value)
        self.config = config or {}

    def read(self, destination, config):
        string_value = config.get(self.name)
        if string_value in [None, "None"]:
            value = copy.deepcopy(self.default_value)
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

    def edit(self, component):
        current_value = self.get_value(component)
        if current_value is None:
            current_value = "None"
        changed, new_value = imgui.input_text(self.name, current_value, imgui.INPUT_TEXT_ENTER_RETURNS_TRUE)
        if changed:
            print(f"NEW: {new_value}")
            self.set_value(component, new_value)

class IntField(Field):
    def parse(self, value):
        return int(value)

    def serialise(self, value):
        return value

    def validate(self, value):
        min_val = self.config.get("min")
        max_val = self.config.get("max")
        if min_val is not None and min_val > value:
            return False
        if max_val is not None and max_val < value:
            return False
        return True

    def edit(self, component):
        current_value = self.get_value(component)
        is_valid = self.validate(current_value)
        if self.config.get("slider"):
            min_value, max_value = self.config.get("slider")
            changed, new_value = imgui.slider_int(self.name, current_value, min_value, max_value)
        else:
            changed, new_value = imgui.input_int(self.name, current_value)
        if not is_valid:
            imgui.same_line()
            imgui.text("Bad value!")
        if changed and self.validate(new_value):
            #print(f"setting {self.name}={new_value}") 
            self.set_value(component, new_value)


class FloatField(Field):
    def parse(self, value):
        return float(value)

    def serialise(self, value):
        return value

    def validate(self, value):
        min_val = self.config.get("min")
        max_val = self.config.get("max")
        if min_val is not None and min_val > value:
            return False
        if max_val is not None and max_val < value:
            return False
        return True

    def edit(self, component):
        current_value = self.get_value(component)
        is_valid = self.validate(current_value)
        if self.config.get("slider"):
            min_value, max_value = self.config.get("slider")
            changed, new_value = imgui.slider_float(self.name, current_value, min_value, max_value)
        else:
            changed, new_value = imgui.input_float(self.name, current_value)
        if not is_valid:
            imgui.same_line()
            imgui.text("Bad value!")
        if changed and self.validate(new_value):
            #print(f"setting {self.name}={new_value}") 
            self.set_value(component, new_value)


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

    def edit(self, component):
        imgui.text(self.name)
        current_value = self.get_value(component)
        for index, entry in enumerate(current_value):
            changed, new_entry = imgui.input_text(f"##{self.name}/{index}", entry)
            if changed:
                current_value[index] = new_entry
                self.set_value(component, current_value)
        if imgui.button(f"add {self.name}"):
            current_value.append("")
            self.set_value(component, current_value)


class V2Field(Field):
    def parse(self, value):
        return V2.parse(value)

    def edit(self, component):
        current_value = self.get_value(component)
        changed, new_values = imgui.input_float2(self.name, current_value.x, current_value.y)
        if changed:
            print(f"V2 -> {self.name}={new_values}") 
            self.set_value(component, V2(*new_values))

class LiteralField(Field):
    def parse(self, value):
        return literal_eval(value)

