from pessimal.engine import math_support as ms
import numpy as np


def test_m44():
    identity_list = ms.m44_get_identity()

    assert identity_list == [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]

    m44 = ms.as44(identity_list)
    assert m44[0][0] == 1

    flattened = ms.as_list(m44)
    assert all(map(lambda x: x[0] == x[1], zip(identity_list, flattened)))

    move_in_y = ms.m44_get_translation(0.0, 10, 0)
    m44_translation = ms.as44(move_in_y)
    assert m44_translation[0][0] == 1
    assert m44_translation[3][0] == 0
    assert m44_translation[3][1] == 10

    assert ms.m44_get_y_rot(0.0)[0] == 1.0
    assert ms.m44_get_y_rot(2.0)[0] < 0.0
    assert ms.m44_get_x_rot(0.0)[0] == 1.0
    assert ms.m44_get_x_rot(2.0)[0] == 1.0
    assert ms.m44_get_x_rot(2.0)[5] < 0.0


def test_normalise():
    original = np.array([2, 0])
    normalised = ms.v_normalize(original)
    assert normalised[0] == 1.0
