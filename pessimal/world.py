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
        self.entities.append(entity)
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

    def update(self, dt):
        while self.scheduled_to_delete:
            target = self.scheduled_to_delete.pop()
            if target in self.entities:
                self.entities.remove(target)
            else:
                print(f"Child entity... {target}")
        for entity in self.entities:
            entity.update(dt)

    def render(self, engine):
        for entity in self.entities:
            entity.render(engine)

