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


def get_json_params(dataset_id):
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
    Return the displayable name of the dataset or undefined if the
    dataset has no human readable name.
    """
    dataset_params = get_ds(dataset_id)
    title = dataset_params.get("title", None)
    if title is None or not title:
        return "undefined"
    return title


# api/datasets/{ds_id}/type
def get_ds_type(dataset_id):
    dataset_params = get_ds(dataset_id)
    layer_type = dataset_params.get("layer_type", None)
    if layer_type is not None:
        return layer_type
    return "undefined"


# api/datasets/{ds_id}/layers/{l_id}/legend_variables/{variable}
def get_legend_variable(dataset_id):
    """
    Return the variable used to color the layer, its units and its min/max values, or
    an empty dict if the legend or the variable used to color the map are not specified.
    """
    dataset_params = get_ds(dataset_id)
    legend = dataset_params.get("legend", {})
    return legend.get("legend_variable", {})


# api/datasets/{ds_id}/openair
def get_openair_link(dataset_id):
    """ Return the address of the dataset on the OpenAir website, or a default link if it is not
    specified"""
    default_link = (
        "https://beta.enermaps.openaire.eu/search/publication?pid=10.3390%2Fen12244789"
    )
    dataset_params = get_ds(dataset_id)
    link = dataset_params.get("openair_link", None)
    if link is None or not link:
        return default_link
    return link


# api/datasets/{ds_id}/layers/{l_id}/style
def get_legend_style(dataset_id):
    """Get the style used to color the map or a default style if the
    legend or the style are undefined
    Return a list of colors used for coloring the layer and their threshold values.
    (color, min_threshold, max_threshold)"""

    def get_sns_color(palette, nb_of_colors):
        color_list = sns.color_palette(palette, nb_of_colors)
        rgb_list = [
            ((int(255 * color[0])), (int(255 * color[1])), (int(255 * color[2])))
            for color in color_list
        ]
        return rgb_list

    dataset_params = get_ds(dataset_id)
    legend = dataset_params.get("legend", None)
    style = legend.get("style", {})
    colors = style.get("colors", None)
    if colors is None:
        default_colors = get_sns_color("flare", 12)
        colors = default_colors

    layer_style = []
    variable = get_legend_variable(dataset_id)
    min_value = variable.get("min", None)
    max_value = variable.get("max", None)
    if min_value is not None and max_value is not None:
        nb_of_colors = len(colors)
        for n, color in enumerate(colors, start=1):
            min_threshold = min_value + (n - 1) * (
                (max_value - min_value) / nb_of_colors
            )
            min_threshold = round(min_threshold, 2)
            max_threshold = min_value + n * ((max_value - min_value) / nb_of_colors)
            max_threshold = round(max_threshold, 2)
            layer_style.append((color, min_threshold, max_threshold))
    else:
        # give all the polygons the same color (first color of the color list)
        color = colors[0]
        layer_style.append((color, min_value, max_value))

    return layer_style


def get_legend(dataset_id):
    ds_type = get_ds_type(dataset_id)
    if ds_type != "vector":
        # TODO how do we display legends for raster datasets?
        return {}

    variable = get_legend_variable(dataset_id)
    style = get_legend_style(dataset_id)
    return {"variable": variable, "style": style}
