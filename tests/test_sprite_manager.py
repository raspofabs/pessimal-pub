from tests.fixtures import f_mock_engine
from pessimal.sprite_manager import SpriteManager

import pytest


def test_sprite_manager(f_mock_engine):
    sm = SpriteManager.get_manager()
    dirtpath = sm.get_sprite("roguelike:dirtpath_")
    assert dirtpath is not None
    coordinate = sm.get_sprite("roguelike:0,3")
    assert coordinate is not None
    unknown = sm.get_sprite("unknown:random")
    assert unknown is None
    incorrect = sm.get_sprite("incorrect")
    assert incorrect is None
    bad_coordinate = sm.get_sprite("roguelike:0,3,5")
    assert bad_coordinate is None

    just_none = sm.get_sprite_or_none(None)
    assert just_none is None
