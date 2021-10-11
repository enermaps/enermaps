import base64

AREA = "area"
VECTOR = "vector"
RASTER = "raster"
CM = "cm"


def encode(value):
    return base64.b64encode(str.encode(value)).decode()


def decode(value):
    return base64.b64decode(str.encode(value)).decode()


def make_unique_layer_name(type, id, variable=None, time_period=None):
    """Make an unique name for a given layer"""

    name = f"{type}/{id}"

    if type in (VECTOR, RASTER):
        if (time_period is not None) and (variable is not None):
            name += f"/{time_period}/{encode(variable)}"
        elif variable is not None:
            name += f"//{encode(variable)}"
        elif time_period is not None:
            name += f"/{time_period}"

    return name


def parse_unique_layer_name(name):
    """Parse the unique name corresponding to a given layer and return its parameters"""

    type, id, *parts = name.split("/")

    variable = None
    time_period = None

    if len(parts) == 2:
        time_period, variable = parts
        if time_period == "":
            time_period = None
    elif len(parts) == 1:
        time_period = parts[0]

    if type in (VECTOR, RASTER):
        id = int(id)

    if time_period is not None:
        time_period = int(time_period)

    if variable is not None:
        variable = decode(variable)

    return (type, id, variable, time_period)


def get_type(name):
    type, *parts = name.split("/")
    return type


def to_folder_path(name):
    type, *parts = name.split("/")

    if type == VECTOR:
        (type, id, variable, time_period) = parse_unique_layer_name(name)
        if time_period is not None:
            return f"{id}/{time_period}"
        else:
            return f"{id}"

    return "/".join(parts).replace("//", "/")
