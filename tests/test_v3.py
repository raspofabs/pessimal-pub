import pytest
import math

from pessimal.v3 import V3


def test_v3_class():
    zero = V3(0, 0, 0)
    assert zero.x == 0.0
    assert zero.y == 0.0
    assert zero.z == 0.0

    one_two_three = V3(1, 2, 3)
    assert one_two_three.x == 1.0
    assert one_two_three.y == 2.0

    assert V3(1, 2, 0) + V3(3, 0, 4) == V3(4, 2, 4)
    assert V3(4, 3, 8) - V3(1, 2, 2) == V3(3, 1, 6)

    assert V3(1, 0.5, 3) * 3 == V3(3, 1.5, 9)

    assert V3(1, 0, 0).mag() == 1.0
    assert V3(1, 2, 2).mag() == 3.0
    assert V3(2, 3, 6).mag() == 7.0
    assert V3(4, 4, 7).mag() == 9.0
    assert V3(1, 4, 8).mag() == 9.0

    assert V3(1, 1, 1).mag() > 1.0
    assert V3(1, 1, 1).mag() < 2.0


def test_v3_casting():
    assert V3(3, 8, 0).as_coord() == (3, 8, 0)
