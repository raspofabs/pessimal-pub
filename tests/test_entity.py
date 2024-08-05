from pessimal.entity import Entity
from tests.components.fixtures import f_simple_world
from tests.fixtures import f_mock_engine
from pessimal.v2 import V2

import pytest


def test_empty_entity():
    empty_entity = Entity(None, {"name": "Empty"})

    # test writing out
    save_config = empty_entity.save_out()    
    assert save_config.get("type") == empty_entity.__class__.__name__
    assert save_config.get("name") == empty_entity.name
    assert save_config.get("size") == empty_entity.size
    assert tuple(eval(save_config.get("start_pos"))) == (0,0)

    assert "Empty" in str(empty_entity)

@pytest.fixture
def f_simple_entity_config():
    return {
            "type": "Entity",
            "name": "Simple",
            "size": 16,
            "start_pos": '[32, 32]',
            "components": [ { 
                 "type": "Orbiter",
                 "centre": '[0.00, 0.00]',
                 "radius": 80,
                 "speed": 4,
                 }, {
                    "colour": '(40, 80, 220)',
                    "type": "SimpleRender",
                    } ],
            "entities": [
                {
                    "type": "Entity",
                    "name": "First",
                    "size": 8,
                    "start_pos": '[8,0]',
                    },
                {
                    "type": "Entity",
                    "name": "Second",
                    "size": 8,
                    "start_pos": '[-16,0]',
                    },
                ],
            }

def test_simple_entity(f_simple_entity_config):
    simple_entity = Entity(None, f_simple_entity_config)

    # test writing out
    save_config = simple_entity.save_out()    

    assert save_config.get("type") == "Entity"
    assert save_config.get("name") == "Simple"
    assert save_config.get("size") == 16
    assert tuple(eval(save_config.get("start_pos"))) == (32,32)

    components = save_config.get("components", [])
    assert len(components) == 2


def test_finding_entities(f_simple_world, f_simple_entity_config):
    simple_entity = f_simple_world.add_entity(f_simple_entity_config)

    #test finding entities
    assert f_simple_world.find_entity_by_name("Simple") == simple_entity

    assert simple_entity.get_pos() == V2(32,32)

    first = f_simple_world.find_entity_by_name("First")
    assert first != simple_entity
    assert first is not None
    assert first.get_pos() == V2(40,32)

    second = f_simple_world.find_entity_by_name("Second")
    assert second is not None
    assert second.get_pos() == V2(16,32)

    third = f_simple_world.find_entity_by_name("Third")
    assert third is None


def test_entity_methods(f_simple_world, f_simple_entity_config, f_mock_engine):
    simple_entity = f_simple_world.add_entity(f_simple_entity_config)

    f_simple_world.start()
    f_simple_world.update(0.1)
    f_simple_world.render(f_mock_engine)
    f_simple_world.stop()


def test_entity():
    empty_entity = Entity(None, None)

    save_config = empty_entity.save_out()    
    assert save_config.get("type") == empty_entity.__class__.__name__
    assert save_config.get("name") == empty_entity.name
    assert save_config.get("size") == empty_entity.size
    assert tuple(eval(save_config.get("start_pos"))) == (0,0)

def test_entity_in_world(f_simple_world):
    entity = f_simple_world.find_entity_by_name("my_entity")
    assert entity is not None
