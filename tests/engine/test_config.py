import pytest
import pessimal.engine.config as cfg
import yaml

@pytest.fixture
def f_config():
    config = {"a": "20%, 50%"}
    return config


def test_load_config(tmp_path, f_config):
    config_path = tmp_path / "config.yaml"

    assert cfg.load_config(config_path) == {}

    with open(config_path, "wt") as yaml_fh:
        yaml.dump(f_config, yaml_fh)
    assert cfg.load_config(config_path) == f_config

def test_x_of_y():
    assert cfg.x_of_y("100%", 50) == 50
    assert cfg.x_of_y("10%", 50) == 5
    assert cfg.x_of_y("20px", 5) == 20
    assert cfg.x_of_y("20px", 1000) == 20
    assert cfg.x_of_y("10", 5) == 10

def test_calculate_tuple(f_config):
    assert cfg.calculate_tuple(f_config, 100, 100, "a", "50%, 20%") == (20, 50)
