from pessimal.components import RoadNetwork
from pessimal.components.road_network import RoadSegment
from pessimal.component import Component
from pessimal.v2 import V2

from tests.fixtures import f_mock_engine
from tests.components.fixtures import f_simple_world

import pytest

def test_road_segment():
    horizontal = RoadSegment(V2(-1,0), V2(1,0))
    assert horizontal.length == 2
    assert horizontal.dir == V2(1,0)

    vertical = RoadSegment(V2(0,-1), V2(0,1))
    assert vertical.length == 2
    assert vertical.dir == V2(0,1)

    assert horizontal.closest_point(V2(0,0)) == V2(0,0)
    assert horizontal.closest_point(V2(0,0.5)) == V2(0,0)
    assert horizontal.closest_point(V2(0,-0.5)) == V2(0,0)
    assert horizontal.closest_point(V2(0,1.5)) == V2(0,0)
    assert horizontal.closest_point(V2(0,-1.5)) == V2(0,0)
    assert horizontal.closest_point(V2(0.5,0)) == V2(0.5,0)
    assert horizontal.closest_point(V2(-0.5,0)) == V2(-0.5,0)
    assert horizontal.closest_point(V2(1.5,0)) == V2(1,0)
    assert horizontal.closest_point(V2(-1.5,0)) == V2(-1,0)

    assert vertical.closest_point(V2(0,0)) == V2(0,0)
    assert vertical.closest_point(V2(0,0.5)) == V2(0,0.5)
    assert vertical.closest_point(V2(0,-0.5)) == V2(0,-0.5)
    assert vertical.closest_point(V2(0,1.5)) == V2(0,1)
    assert vertical.closest_point(V2(0,-1.5)) == V2(0,-1)
    assert vertical.closest_point(V2(0.5,0)) == V2(0,0)
    assert vertical.closest_point(V2(-0.5,0)) == V2(0,0)
    assert vertical.closest_point(V2(1.5,0)) == V2(0,0)
    assert vertical.closest_point(V2(-1.5,0)) == V2(0,0)


@pytest.fixture
def f_road_config():
    return {
            "type": "Entity",
            "name": "Roads",
            "size": 80.0,
            "start_pos": '[0.00, 0.00]',
            "components":[
                {
                    "type": "RoadNetwork",
                    "roads": {
                        "road_1": "-40, 0, 40, 0",
                        "road_2": "10, -100, 10, 20",
                        },
                    },
                ],
            }


def test_road_network(f_mock_engine, f_simple_world, f_road_config):
    road_network_entity = f_simple_world.add_entity(f_road_config)
    assert road_network_entity is not None

    road_network_component = road_network_entity.get_component("RoadNetwork")
    assert road_network_component is not None


def test_road_network_render(f_mock_engine, f_simple_world, f_road_config):
    f_simple_world.add_entity(f_road_config)

    # default render
    f_simple_world.render(f_mock_engine)

    # not rendering
    f_mock_engine.toggle_culling()
    f_simple_world.render(f_mock_engine)

