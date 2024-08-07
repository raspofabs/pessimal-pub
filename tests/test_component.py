import pessimal.component as pc
import pessimal.components as pcs

from tests.fixtures import f_mock_engine

import pytest


# diamond inheritance components just for testing recursion code


class Left(pc.Component):
    def __init__(self, config: dict):
        super().__init__(config)


class Right(pc.Component):
    def __init__(self, config: dict):
        super().__init__(config)


class Diamond(Left, Right):
    def __init__(self, config: dict):
        super().__init__(config)


def test_reflection():
    all_components = pc.Component.get_all_component_types()

    # check a few are present
    assert pcs.WorkCentre in all_components
    assert pcs.Player in all_components
    assert pcs.Character in all_components

    # check a few are not present
    assert pc.Component not in all_components
    assert int not in all_components

    assert pcs.Building == pc.Component.get_class_from_name("Building")
    assert None == pc.Component.get_class_from_name("Builder")


def test_basics():
    # plain component
    component = pc.Component(None)
    component.start()
    component.update(0.1)
    component.render(None)
    component.stop()


def test_construction(f_mock_engine):
    unknown = pc.Component.create({}, None)
    assert unknown is None
    nothing = pc.Component.create({"type": "Nothing"}, None)
    assert nothing is None
