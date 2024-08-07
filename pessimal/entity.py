import pygame
import sys
import os
import yaml
from pessimal.v2 import V2
from pessimal.component import Component
from pessimal.field import V2Field, Field, FloatField


class Entity(Component):
    fields = [
        V2Field("start_pos", V2(0, 0)),
        Field("name", "unnamed"),
        FloatField("size", 1.0, config={"slider": (0.0, 200.0)}),
    ]

    def __init__(self, parent, config):
        super().__init__(parent, config)

        if hasattr(parent, "entities"):
            parent.entities.append(self)
        if config is None:
            config = {}
        self.start_pos = V2.parse(config.get("start_pos", "0,0"))
        self.pos = self.start_pos
        self.name = config.get("name", "")
        self.size = float(config.get("size", "4"))
        # self.size = V2(size, size)
        self.entities = []
        self.components = []

        for component_config in config.get("components", []):
            component = Component.create(component_config, self)
            assert component, f"Error with component: {component_config=}"
            self.components.append(component)
        # we want to allow hierarchies
        for entity_config in config.get("entities", []):
            sub_entity = Component.create(entity_config, self)
            assert sub_entity, f"Error with sub_entity: {entity_config=}"
            self.entities.append(sub_entity)

    def save_out(self):
        config = super().save_out()

        if self.components:
            config["components"] = []
            for component in self.components:
                config["components"].append(component.save_out())
        if self.entities:
            config["entities"] = []
            for entity in self.entities:
                config["entities"].append(entity.save_out())
        return config

    def get_entities(self):
        return self.entities

    def find_entity_by_name(self, name):
        for entity in self.get_entities():
            if entity.name == name:
                return entity
            if found := entity.find_entity_by_name(name):
                return found
        return None

    def find_entities_by_component(self, component_name):
        entities = []
        for entity in self.get_entities():
            if entity.get_component(component_name) is not None:
                entities.append(entity)
        return entities

    def __str__(self):
        component_names = ", ".join([c.__class__.__name__ for c in self.components])
        return f"{self.name} - {self.pos}: {component_names}"

    def start(self):
        self.pos = self.start_pos
        for component in self.components:
            component.start()

    def stop(self):
        self.pos = self.start_pos
        for component in self.components:
            component.stop()

    def get_pos(self):
        if self.parent is not None:
            return self.parent.get_pos() + self.pos
        return self.pos

    def get_size(self):
        return V2(self.size, self.size)

    def update(self, dt):
        for component in self.components:
            component.update(dt)
        for entity in self.entities:
            entity.update(dt)

    def render(self, engine):
        for component in self.components:
            component.render(engine)
        for entity in self.entities:
            entity.render(engine)

    def get_component(self, component_name):
        for component in self.components:
            if component.__class__.__name__ == component_name:
                return component
        return None
