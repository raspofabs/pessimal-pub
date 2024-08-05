from pessimal.world import World
from tests.components.fixtures import f_simple_world


def test_world_state(f_simple_world):
    f_simple_world.find_entity_by_name("my_entity")

    f_simple_world.start()
    f_simple_world.update(0.1)
    f_simple_world.render(None)
    f_simple_world.stop()


def test_world_connection(f_simple_world):
    entity = f_simple_world.find_entity_by_name("my_entity")
    found_world = entity.get_world()
    assert found_world == f_simple_world


def test_saveout(f_simple_world):
    world_data = {"entities":[]}
    f_simple_world.save_out(world_data)
    assert len(world_data.get("entities")) == 1
