from pessimal.component import Component
import pessimal.components
from pessimal.entity import Entity


class World(Entity):
    def __init__(self):
        super().__init__(None, {})
        self.scheduled_to_delete = []

    def get_world(self):
        return self

    def add_entity(self, entity_config):
        entity = Entity(self, entity_config)
        return entity

    def delete_entity(self, entity_to_delete):
        self.scheduled_to_delete.append(entity_to_delete)

    def save_out(self, config):
        for entity in self.entities:
            config["entities"].append(entity.save_out())

    def start(self):
        for entity in self.entities:
            entity.start()

    def stop(self):
        for entity in self.entities:
            entity.stop()

    @staticmethod
    def delete_entity_from_tree(node, target):
        if node is None:
            return False
        if target in node.entities:
            node.entities.remove(target)
            return True
        for sub_node in node.entities:
            if World.delete_entity_from_tree(sub_node, target):
                return True
        return False

    def update(self, dt):
        while self.scheduled_to_delete:
            target = self.scheduled_to_delete.pop()
            self.delete_entity_from_tree(self, target)
        for entity in self.entities:
            entity.update(dt)

    def render(self, engine):
        for entity in self.entities:
            entity.render(engine)
