from pessimal.field import (
    Field,
    IntField,
    FloatField,
    V2Field,
    ListField,
    DictField,
)


class PlaygroundClass:
    """This class is empty, just so we can detect fields doing their work."""

    def __init__(self):
        pass


def test_field():
    test_object = PlaygroundClass()

    assert not hasattr(test_object, "test_field")
    test_field = Field("test_field", "default value")

    test_field.read(test_object, {})

    # verify the attribute now exists
    assert hasattr(test_object, "test_field")
    assert test_object.test_field == "default value"
    assert test_field.get_value(test_object) == test_object.test_field

    # set a new value (not load in)
    test_field.set_value(test_object, "new value")

    # get value and get serialisable form
    assert test_field.get_value(test_object) == "new value"
    assert test_field.store(test_object) == "new value"

    # read real value
    test_field.read(test_object, {"test_field": "construction value"})
    assert test_object.test_field == "construction value"


def test_int_field():
    test_object = PlaygroundClass()

    assert not hasattr(test_object, "test_field")
    test_field = IntField("test_field", 30)

    test_field.read(test_object, {})

    # verify the attribute now exists
    assert hasattr(test_object, "test_field")
    assert test_object.test_field == 30

    # read real value
    test_field.read(test_object, {"test_field": 101})
    assert test_object.test_field == 101

    # test input validation
    limited_field = IntField("test_field", 30, config={"min": 0, "max": 20})
    assert not limited_field.validate(-1)
    assert limited_field.validate(0)
    assert limited_field.validate(20)
    assert not limited_field.validate(21)


def test_float_field():
    test_object = PlaygroundClass()

    assert not hasattr(test_object, "test_field")
    test_field = FloatField("test_field", 30)

    test_field.read(test_object, {})

    # verify the attribute now exists
    assert hasattr(test_object, "test_field")
    assert test_object.test_field == 30

    # test input validation
    limited_field = FloatField("test_field", 30, config={"min": 0, "max": 20})
    assert not limited_field.validate(-1)
    assert limited_field.validate(0)
    assert limited_field.validate(20)
    assert not limited_field.validate(21)


def test_dict_field():
    test_object = PlaygroundClass()

    assert not hasattr(test_object, "test_field")
    default_value = {"a": 1, "b": 4}
    test_field = DictField("test_field", default_value)

    # read from dict
    test_field.read(test_object, {})

    # verify the attribute now exists
    assert hasattr(test_object, "test_field")
    assert test_object.test_field["a"] == 1
    assert test_object.test_field["b"] == 4

    # read from dict
    test_field.read(test_object, {"test_field": {"a": 2}})
    assert test_object.test_field["a"] == 2

    # read from json
    test_field.read(test_object, {"test_field": '{"a": 3}'})
    assert test_object.test_field["a"] == 3

    # serialise just returns a dict
    assert test_field.store(test_object) == {"a": 3}


def test_list_field():
    test_object = PlaygroundClass()

    assert not hasattr(test_object, "test_field")
    default_value = ["a", "b"]
    test_field = ListField("test_field", default_value)

    # read from list
    test_field.read(test_object, {})

    # verify the attribute now exists
    assert hasattr(test_object, "test_field")
    assert test_object.test_field == ["a", "b"]

    # read from list
    test_field.read(test_object, {"test_field": [1, 2, 3]})
    assert test_object.test_field == [1, 2, 3]

    # read from json
    test_field.read(test_object, {"test_field": "[1,2,3,4]"})
    assert test_object.test_field == [1, 2, 3, 4]

    # serialise just returns a list
    assert test_field.store(test_object) == [1, 2, 3, 4]


def test_invalid_parse():
    test_object = PlaygroundClass()

    assert not hasattr(test_object, "test_field")
    default_value = ["a"]
    test_field = ListField("test_field", default_value)

    try:
        # read from list
        test_field.read(test_object, {"test_field": {"dict": "value"}})
        assert False, "Should have died here using a dict for a list field."
    except ValueError:
        pass

    # verify the attribute now exists
    assert not hasattr(test_object, "test_field")
