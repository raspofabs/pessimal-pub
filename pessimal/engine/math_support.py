import numpy as np

def as44(m44list):
    return np.array(m44list).reshape((4, 4))


def as_list(m44):
    return [element for row in m44 for element in row]


def m44_get_identity():
    return [
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0,
    ]


def m44_get_translation(x: float, y: float, z: float):
    return [
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        x, y, z, 1.0]


def m44_get_y_rot(y: float):
    return [
        np.cos(y), 0.0, -np.sin(y), 0.0,
        0.0, 1.0, 0.0, 0.0,
        np.sin(y), 0.0, np.cos(y), 0.0,
        0.0, 0.0, 0.0, 1.0]


def m44_get_x_rot(x: float):
    return [
        1.0, 0.0, 0.0, 0.0,
        0.0, np.cos(x), np.sin(x), 0.0,
        0.0, -np.sin(x), np.cos(x), 0.0,
        0.0, 0.0, 0.0, 1.0]


def v_normalize(v):
    normalized_v = v / np.sqrt(np.sum(v ** 2))
    return normalized_v

