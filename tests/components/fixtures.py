from pessimal.world import World
import pytest


@pytest.fixture
def f_simple_world():
    world = World()
    world.add_entity({"name":"my_entity"})
    return world

