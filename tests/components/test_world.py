from pessimal.world import World, Entity
from tests.components.fixtures import f_simple_world


def test_world_state(f_simple_world):
    test_entity = f_simple_world.find_entity_by_name("my_entity")
    assert test_entity is not None

    f_simple_world.start()
    f_simple_world.update(0.1)
    f_simple_world.render(None)
    f_simple_world.stop()

    f_simple_world.delete_entity(test_entity)

    f_simple_world.update(0.1)

    test_entity = f_simple_world.find_entity_by_name("my_entity")
    assert test_entity is None

def test_world_connection(f_simple_world):
    entity = f_simple_world.find_entity_by_name("my_entity")
    found_world = entity.get_world()
    assert found_world == f_simple_world


def test_saveout(f_simple_world):
    world_data = {"entities": []}
    f_simple_world.save_out(world_data)
    assert len(world_data.get("entities")) == 1

def test_entity_delete():
    assert not World.delete_entity_from_tree(None, None)

    base = Entity(None, {"name": "base"})
    first_child = Entity(base, {"name": "first_child"})
    second_child = Entity(base, {"name": "second_child"})
    sub_child = Entity(second_child, {"name": "sub_child"})

    assert len(base.entities) == 2
    assert len(first_child.entities) == 0
    assert len(second_child.entities) == 1

    assert World.delete_entity_from_tree(base, sub_child)
    assert World.delete_entity_from_tree(base, first_child)
