import hashlib

import seaborn as sns

from app.data_integration.data_config import DATASETS_DIC


def get_ds(dataset_id):
    """Return the dataset default parameters as a dict or an
    empty dict if there is no default parameters for this dataset"""
    for value in DATASETS_DIC.values():
        if value.get("id", None) == dataset_id:
            return value
    else:
        return {}


# TODO delete this function and the json parameters
def get_json_params(dataset_id):
    """ """
    dataset_params = get_ds(dataset_id)
    return dataset_params.get("json_params", None)


# api/datasets/ GET
def get_ds_ids():
    """
    Return a list containg the IDs of all the datasets (same ID as in the DB).
    """
    ids = []
    for value in DATASETS_DIC.values():
        id = value.get("id", None)
        if id:
            ids.append(id)
    return ids


# api/datasets/{ds_id}/name
def get_ds_title(dataset_id):
    """
    Return the displayable name of the dataset or "undefined" if the
    dataset has no human readable name.
    """
    dataset_params = get_ds(dataset_id)
    title = dataset_params.get("title", None)
    if title is None or not title:
        return "undefined"
    return title


# api/datasets/{ds_id}/type
def get_ds_type(dataset_id):
    """Get the dataset type (vector or raster) and the dataset
    data type (numerical, categorical), or "undefined" if the configuration
    file does not contain this information"""
    dataset_params = get_ds(dataset_id)
    layer_type = dataset_params.get("layer_type", None)
    data_type = dataset_params.get("data_type", None)
    if layer_type is not None:
        return layer_type, data_type
    return "undefined", "undefined"


# api/datasets/{ds_id}/layers/{l_id}/legend_variables/{variable}
def get_legend_variable(dataset_id):
    """
    Return the layer variable used to color the layer, its units and its min/max values, or
    an empty dict if the legend or the variable used to color the map are not specified.
    """
    dataset_params = get_ds(dataset_id)
    empty_legend_variable = {
        "variable": "No legend defined",
        "units": None,
        "min": None,
        "max": None,
    }
    legend = dataset_params.get("legend", {})
    legend_variable = legend.get("legend_variable", empty_legend_variable)
    return legend_variable


# api/datasets/{ds_id}/openair
def get_openair_link(dataset_id):
    """Return the address of the dataset on the OpenAir website, or a default link if it is not
    specified"""
    default_link = "https://beta.openaire.eu/"

    dataset_params = get_ds(dataset_id)
    link = dataset_params.get("shared_id", None)
    if link is None or not link:
        return default_link

    # Construct the OpenAIRE dataset address
    shared_id_hash = hashlib.md5(link.encode())  # nosec
    link = "https://beta.enermaps.openaire.eu/search/dataset?datasetId=enermaps____::{}".format(
        shared_id_hash.hexdigest()
    )
    return link


# api/datasets/{ds_id}/layers/{l_id}/style
def get_legend_style(dataset_id):
    """Get the style used to color the map or a default style if the
    legend or the style are undefined
    Return a list of colors used for coloring the layer and their threshold values.
    (color, min_threshold, max_threshold)"""

    dataset_params = get_ds(dataset_id)
    # Get the legend information needed to create the legend
    legend = dataset_params.get("legend", {})
    style = legend.get("style", {})

    # Get a color list using Seaborn
    def get_sns_color(palette, nb_of_colors):
        color_list = sns.color_palette(palette, nb_of_colors)
        # This conversion is needed by Mapnik
        rgb_list = [
            ((int(255 * color[0])), (int(255 * color[1])), (int(255 * color[2])))
            for color in color_list
        ]
        return rgb_list

    layer_type, data_type = get_ds_type(dataset_id)

    # If the layer contains categorical data, return a list
    # of color code with its associated color and legend
    if data_type == "categorical":
        classes = style.get("classes", None)
        classes_list = []
        if classes is not None:
            # key: raster color code
            # value : (color_rgb_code, category_name)
            for key, value in classes.items():
                classes_list.append((key, value))
        return classes_list

    colors = style.get("colors", None)
    if layer_type == "vector":
        if colors is None:
            color_palet = "flare"
            nb_of_colors = 8
        else:
            color_palet = colors.get("color_palet", "flare")
            nb_of_colors = colors.get("nb_of_colors", 8)
        color_list = sns.color_palette(color_palet, nb_of_colors)
        color_list = [
            ((int(255 * color[0])), (int(255 * color[1])), (int(255 * color[2])))
            for color in color_list
        ]
    elif layer_type == "raster":
        if colors is None:
            color = (1, 0, 0)  # Default red
            nb_of_colors = 8
        else:
            color = colors.get("color", (1, 0, 0))
            nb_of_colors = colors.get("nb_of_colors", 8)
        color_list = sns.dark_palette(color, n_colors=nb_of_colors, input="rgb")
        color_list = [
            ((int(255 * color[0])), (int(255 * color[1])), (int(255 * color[2])))
            for color in color_list
        ]

    # If the layer data type is not categorical, return a list of color associated
    # with the min and max values of the interval that is colorized with this color
    layer_style = []
    variable = get_legend_variable(dataset_id)
    min_value = variable.get("min", None)
    max_value = variable.get("max", None)
    if min_value is not None and max_value is not None:
        for n, color in enumerate(color_list, start=1):
            min_threshold = min_value + (n - 1) * (
                (max_value - min_value) / nb_of_colors
            )
            min_threshold = round(min_threshold, 2)
            max_threshold = min_value + n * ((max_value - min_value) / nb_of_colors)
            max_threshold = round(max_threshold, 2)
            layer_style.append((color, min_threshold, max_threshold))

    return layer_style


def get_legend(dataset_id):
    """
    Return the layer variable used to colorize the layer and the legend style.
    """
    variable = get_legend_variable(dataset_id)
    layer_type, data_type = get_ds_type(dataset_id)
    style = get_legend_style(dataset_id)
    return {"variable": variable, "style": style, "data_type": data_type}
