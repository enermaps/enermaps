import base64

AREA = "area"
VECTOR = "vector"
RASTER = "raster"
CM = "cm"


def encode(value):
    return base64.urlsafe_b64encode(str.encode(value)).decode()


def decode(value):
    return base64.urlsafe_b64decode(str.encode(value)).decode()


def make_unique_layer_name(type, id, variable=None, time_period=None, task_id=None):
    """Make an unique name for a given layer"""

    name = f"{type}/{id}"

    if type in (VECTOR, RASTER):
        if (time_period is not None) and (variable is not None):
            name += f"/{time_period}/{encode(variable)}"
        elif variable is not None:
            name += f"//{encode(variable)}"
        elif time_period is not None:
            name += f"/{time_period}"

    elif type == CM:
        if task_id is None:
            return None

        name += f"/{task_id}"

    return name


def parse_unique_layer_name(name):
    """Parse the unique name corresponding to a given layer and return its parameters"""

    type, id, *parts = name.split("/")

    variable = None
    time_period = None
    task_id = None

    if type in (VECTOR, RASTER):
        id = int(id)

        if len(parts) == 2:
            time_period, variable = parts
            if time_period == "":
                time_period = None
        elif len(parts) == 1:
            time_period = parts[0]

    elif type == CM:
        if len(parts) != 1:
            return (None, None, None, None, None)

        task_id = parts[0]

    if time_period is not None:
        time_period = int(time_period)

    if variable is not None:
        variable = decode(variable)

    return (type, id, variable, time_period, task_id)


def get_type(name):
    type, *parts = name.split("/")
    return type


def to_folder_path(name):
    type, *parts = name.split("/")

    if type == VECTOR:
        (_, id, _, time_period, _) = parse_unique_layer_name(name)
        if time_period is not None:
            return f"{id}/{time_period}"
        else:
            return f"{id}"

    elif type == CM:
        (_, id, _, _, task_id) = parse_unique_layer_name(name)

        prefix = task_id.split("-")[0]
        parts = [id]

        for i in range(0, len(prefix), 2):
            parts.append(prefix[i : i + 2])

        parts.append(task_id)
        return "/".join(parts)

    return "/".join(parts).replace("//", "/")
