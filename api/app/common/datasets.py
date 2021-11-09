from datetime import datetime

from app.models import storage

from . import path


def convert(parameters):
    # Ensure all fields have the format we want
    params = parameters["parameters"]

    for field in ("variables", "time_periods", "levels"):
        if (field not in params) or (params[field] is None):
            params[field] = []

    for field in ("fields",):
        if (field not in params) or (params[field] is None):
            params[field] = {}

    for field in ("temporal_granularity", "start_at", "min_zoom_level"):
        if field not in params:
            params[field] = None

    field = "end_at"
    if field not in params:
        if field in parameters:
            params[field] = parameters[field]
        else:
            params[field] = None

    for field in ("default_parameters",):
        if (field not in parameters) or (parameters[field] is None):
            parameters[field] = {}

    return {
        "variables": params["variables"],
        "time_periods": [str(x) for x in params["time_periods"]],
        "fields": params["fields"],
        "levels": params["levels"],
        "temporal_granularity": params["temporal_granularity"],
        "start_at": params["start_at"],
        "end_at": params["end_at"],
        "default_parameters": parameters["default_parameters"],
        "min_zoom_level": params["min_zoom_level"],
    }


def process_parameters(parameters, dataset_id=None, is_raster=False):
    _process_time_periods(parameters)

    if dataset_id is not None:
        if not is_raster:
            combinations = _get_valid_combinations(dataset_id)
            parameters["valid_combinations"] = combinations

            if combinations is not None:
                variables = []
                for key, v in combinations.items():
                    variables.extend(v)
                    variables = list(set(variables))

                parameters["variables"] = variables


def _get_valid_combinations(dataset_id):
    layer_name = path.make_unique_layer_name(path.VECTOR, dataset_id)
    storage_instance = storage.create(layer_name)
    return storage_instance.get_combinations(layer_name)


def _process_time_periods(parameters):
    # Custom temporal granularity: assume the time periods are fixed
    if parameters["temporal_granularity"] == "custom":
        if "start_at" in parameters["default_parameters"]:
            del parameters["default_parameters"]["start_at"]

        return

    # Yearly temporal granularity: generate the corresponding time periods
    if parameters["temporal_granularity"] == "year":
        start = datetime.strptime(parameters["start_at"], "%Y-%m-%d %H:%M")
        end = datetime.strptime(parameters["end_at"], "%Y-%m-%d %H:%M")
        parameters["time_periods"] = [str(x) for x in range(start.year, end.year + 1)]
        parameters["temporal_granularity"] = "custom"

        if "start_at" in parameters["default_parameters"]:
            del parameters["default_parameters"]["start_at"]

        return

    # Monthly temporal granularity: generate the corresponding time periods if there are
    # not too many
    if parameters["temporal_granularity"] == "month":
        start = datetime.strptime(parameters["start_at"], "%Y-%m-%d %H:%M")
        end = datetime.strptime(parameters["end_at"], "%Y-%m-%d %H:%M")

        nb_months = (end.year - start.year) * 12 + (end.month - start.month) + 1
        if nb_months > 12:
            return

        time_periods = []

        if start.year != end.year:
            while start <= end:
                time_periods.append(f"{start.year:04d}-{start.month:02d}")

                if start.month < 12:
                    start = datetime(start.year, start.month + 1, 1)
                else:
                    start = datetime(start.year + 1, 1, 1)
        else:
            time_periods = [f"{x:02d}" for x in range(start.month, end.month + 1)]

        parameters["time_periods"] = time_periods
        parameters["temporal_granularity"] = "custom"

        if "start_at" in parameters["default_parameters"]:
            del parameters["default_parameters"]["start_at"]

        return

    # Bi-annual temporal granularity: generate the corresponding time periods
    if parameters["temporal_granularity"] == "six-month":
        start = datetime.strptime(parameters["start_at"], "%Y-%m-%d %H:%M")
        end = datetime.strptime(parameters["end_at"], "%Y-%m-%d %H:%M")

        time_periods = []

        while start <= end:
            time_periods.append(f"{start.year:04d}-{start.month:02d}")

            if start.month < 7:
                start = datetime(start.year, start.month + 6, 1)
            else:
                start = datetime(start.year + 1, start.month - 6, 1)

        parameters["time_periods"] = time_periods
        parameters["temporal_granularity"] = "custom"

        if "start_at" in parameters["default_parameters"]:
            del parameters["default_parameters"]["start_at"]

        return
