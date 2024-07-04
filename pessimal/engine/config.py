import yaml

def load_config():
    try:
        with open("config.yaml") as fh:
            config = yaml.safe_load(fh)
            return config
    except FileNotFoundError:
        pass
    return {}


def x_of_y(factor, value):
    if factor.endswith("%"):
        percentage = float(factor[:-1])
        return value * percentage / 100.0
    if factor.endswith("px"):
        return int(factor.rstrip("px"))
    return int(factor)


def calculate_tuple(config, w, h, name, default):
    setting = config.get(name, default)
    ws, hs = [x.strip() for x in setting.split(",")]

    return x_of_y(ws, w), x_of_y(hs, h)

