import pytest
import math

from pessimal.v2 import V2

def test_v2_parse():
    assert V2.parse("1,2") == V2(1,2)
    assert V2.parse(None) == V2(0,0)
    try:
        V2.parse("abc")
        assert False
    except ValueError:
        pass

def test_v2_class():
    zero = V2(0, 0)
    assert zero.x == 0.0
    assert zero.y == 0.0

    assert str(V2(3, 4)) == "[3.00, 4.00]"

    one_two = V2(1, 2)
    assert one_two.x == 1.0
    assert one_two.y == 2.0
    
    # arithmetic
    assert V2(1, 2) + V2(3, 0) == V2(4, 2)
    assert V2(4, 3) - V2(1, 2) == V2(3, 1)

    assert V2(1, 0.5) * 3 == V2(3, 1.5)

    assert -V2(1, 4) == V2(-1, -4)
    assert 2 * V2(2, 3) == V2(4, 6)

    # magnitude
    assert V2(1, 0).mag() == 1.0
    assert V2(3, 4).mag() == 5.0
    assert V2(5, 12).mag() == 13.0

    assert V2(1, 1).mag() > 1.0
    assert V2(1, 1).mag() < 2.0

    # normals
    assert V2(3, 0).normal() == V2(1, 0)
    assert V2(0, 3).normal() == V2(0, 1)
    sqrthalf = math.sqrt(0.5)
    diagonal = V2(2, 2).normal()
    assert diagonal.x == diagonal.y
    assert diagonal.x == pytest.approx(sqrthalf)
    assert diagonal.y == pytest.approx(sqrthalf)

    # linalg
    assert V2(2, 0).rot90() == V2(0, 2)
    assert V2(0, 2).rot90() == V2(-2, 0)
    assert V2(-4, -2).rot90() == V2(2, -4)

    assert V2(1, 0).dot(V2(0, 2)) == 0.0
    assert V2(1, 1).dot(V2(2, 2)) == 4.0
    assert V2(1, 0).dot(V2(2, 2)) == 2.0
    assert V2(sqrthalf, sqrthalf).dot(V2(2, 2)) == math.sqrt(8)

    assert V2(1, 0).cross(V2(1, 0)) == 0.0
    assert V2(1, 0).cross(V2(0, 1)) == 1.0


def test_v2_casting():
    assert V2(3, 8).as_coord() == (3, 8)
