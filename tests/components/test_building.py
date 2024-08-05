from pessimal.components import Building
from pessimal.component import Component
from pessimal.v2 import V2

from tests.fixtures import f_mock_engine
from tests.components.fixtures import f_simple_world


building_config = {
        "type": "Entity",
        "name": "Wide home",
        "size": 80.0,
        "start_pos": '[0.00, 0.00]',
        "components":[
            {
                "type": "Building",
                "name": "abode",
                "depth": 4,
                "storeys": 3,
                "width": 6,
                "door_x_pos": 3,
                }
            ],
        }


def test_building(f_mock_engine, f_simple_world):
    building_entity = f_simple_world.add_entity(building_config)
    assert building_entity is not None

    building_component = building_entity.get_component("Building")
    assert building_component is not None

    assert building_component.get_door_pos() == V2(3*16, 0)

def test_building_render(f_mock_engine, f_simple_world):
    f_simple_world.add_entity(building_config)

    # default render
    f_simple_world.render(f_mock_engine)

    # not rendering
    f_mock_engine.toggle_culling()
    f_simple_world.render(f_mock_engine)
