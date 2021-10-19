"""Functions related to the "GetMap" operation of the Web Map Service (WMS)"""

import shutil

import mapnik
import seaborn as sns

from app.common import client, path
from app.models import geofile
from app.models.wms import utils


def get_mapnik_map(normalized_args):
    """Return the Mapnik object (with hardcoded symbology/rule)."""

    projection = utils.parse_projection(normalized_args)

    size = utils.parse_size(normalized_args)
    mp = mapnik.Map(size.width, size.height, "+init=" + projection)

    # Style for lines
    line_style, line_style_name = make_line_style()
    mp.append_style(line_style_name, line_style)
    mp.legend_images_folders = []

    # Get the list of the layers to display
    layers = utils.parse_layers(normalized_args)
    for layer_name in layers:
        layer = geofile.load(layer_name)
        if layer is None:
            return None

        mapnik_layers = layer.as_mapnik_layers()
        if (mapnik_layers is None) or (len(mapnik_layers) == 0):
            return None

        legend_style = None
        legend_style_name = None

        if path.get_type(layer_name) in (path.RASTER, path.VECTOR, path.CM):
            (
                legend_style,
                legend_style_name,
                legend_images_folder,
            ) = create_style_from_legend(layer_name, layer, mapnik_layers[0])

            if legend_images_folder is not None:
                mp.legend_images_folders.append(legend_images_folder)

        if legend_style is not None:
            mp.append_style(legend_style_name, legend_style)

        for mapnik_layer in mapnik_layers:
            mapnik_layer.styles.append(line_style_name)

            if legend_style is not None:
                mapnik_layer.styles.append(legend_style_name)

            mp.layers.append(mapnik_layer)

    return mp


def delete_image_folders(mp):
    for folder in mp.legend_images_folders:
        shutil.rmtree(folder)


def create_style_from_legend(layer_name, layer, mapnik_layer):
    (type, layer_id, variable, _, _) = path.parse_unique_layer_name(layer_name)

    # Get the layer style and type
    if type in (path.VECTOR, path.RASTER):
        legend = client.get_legend(layer_name, ttl_hash=client.get_ttl_hash(10))
    elif type == path.CM:
        legend = geofile.get_cm_legend(layer_name)
    else:
        legend = None

    if (legend is None) or (len(legend["symbology"]) == 0):
        legend = create_default_legend(type)

    mapnik_style = None
    style_name = None
    legend_images_folder = None

    if type == path.VECTOR:
        if variable is None:
            variables = [
                x
                for x in mapnik_layer.datasource.fields()
                if x.startswith("__variable__")
            ]
            if len(variables) > 0:
                variable = variables[0].replace("__variable__", "")

        if mapnik_layer.datasource.geometry_type() is mapnik.DataGeometryType.Polygon:
            mapnik_style, style_name = make_polygon_style(variable, legend)
        else:
            legend_images, legend_images_folder = layer.get_legend_images(legend)
            mapnik_style, style_name = make_point_style(variable, legend, legend_images)

    elif type in (path.RASTER, path.CM):
        mapnik_style, style_name = make_raster_style(legend)

    return (mapnik_style, style_name, legend_images_folder)


def create_default_legend(type):
    legend = {"symbology": []}

    min_value = 1 if type in (path.RASTER, path.CM) else 0
    max_value = 255
    color = (1, 0, 0)  # Default red
    nb_of_colors = 8

    color_list = sns.dark_palette(color, n_colors=nb_of_colors, input="rgb")
    color_list = [
        (
            (int(255 * color[0])),
            (int(255 * color[1])),
            (int(255 * color[2])),
        )
        for color in color_list
    ]

    for n, color in enumerate(color_list):
        min_threshold = min_value + n * ((max_value - min_value) / nb_of_colors)
        min_threshold = round(min_threshold, 2)
        legend["symbology"].append(
            {
                "red": color[0],
                "green": color[1],
                "blue": color[2],
                "value": min_threshold,
                "opacity": 1.0,
            }
        )

    return legend


def make_line_style():
    """
    Add a black line style for contours of polygon layers
    """
    mapnik_style = mapnik.Style()
    rule = mapnik.Rule()
    line_symbolizer = mapnik.LineSymbolizer()
    line_symbolizer.stroke = mapnik.Color("black")
    line_symbolizer.stroke_width = 1.0
    rule.symbols.append(line_symbolizer)
    mapnik_style.rules.append(rule)
    return mapnik_style, "line_style"


def make_raster_style(legend):
    """
    Make a style for colorizing numerical rasters.
    Return the style and the style name.
    """
    mapnik_style = mapnik.Style()
    rule = mapnik.Rule()
    raster_symb = mapnik.RasterSymbolizer()
    raster_colorizer = mapnik.RasterColorizer(
        mapnik.COLORIZER_LINEAR, mapnik.Color("transparent")
    )

    # Add a "stop value" and the associated color for each color of the layer
    symbol = legend["symbology"][0]

    if isinstance(symbol["value"], str):
        for symbol in legend["symbology"]:
            color = mapnik.Color(
                int(symbol["red"]),
                int(symbol["green"]),
                int(symbol["blue"]),
            )

            raster_colorizer.add_stop(int(symbol["value"]), color)

    else:
        for symbol in legend["symbology"]:
            color = mapnik.Color(
                int(symbol["red"]),
                int(symbol["green"]),
                int(symbol["blue"]),
            )

            raster_colorizer.add_stop(symbol["value"], mapnik.COLORIZER_LINEAR, color)

    raster_symb.colorizer = raster_colorizer
    rule.symbols.append(raster_symb)
    mapnik_style.rules.append(rule)
    return mapnik_style, "num_raster_style"


def make_polygon_style(variable, legend):
    """
    Make a style for vector polygons
    """

    def _add_rule(mapnik_style, expression, color, opacity):
        polygon_symb = mapnik.PolygonSymbolizer()
        polygon_symb.fill = color
        polygon_symb.fill_opacity = opacity

        rule = mapnik.Rule()
        rule.filter = mapnik.Expression(expression)
        rule.symbols.append(polygon_symb)
        mapnik_style.rules.append(rule)

    mapnik_style = mapnik.Style()

    symbol = legend["symbology"][0]

    min_threshold = symbol["value"]
    opacity = symbol["opacity"]

    color = mapnik.Color(
        int(symbol["red"]),
        int(symbol["green"]),
        int(symbol["blue"]),
    )

    for symbol in legend["symbology"][1:]:
        max_threshold = symbol["value"]
        expression = (
            f"[__variable__{variable}] < {max_threshold} and [__variable__{variable}]"
            f" >= {min_threshold}"
        )

        _add_rule(mapnik_style, expression, color, opacity)

        min_threshold = max_threshold
        opacity = symbol["opacity"]

        color = mapnik.Color(
            int(symbol["red"]),
            int(symbol["green"]),
            int(symbol["blue"]),
        )

    expression = f"[__variable__{variable}] >= {min_threshold}"
    _add_rule(mapnik_style, expression, color, opacity)

    return mapnik_style, "vector_polygon_style"


def make_point_style(variable, legend, legend_images):
    """
    Make a style for vector points
    """

    def _add_rule(mapnik_style, expression, index):
        pt_symbolizer = mapnik.PointSymbolizer()
        pt_symbolizer.file = legend_images[index]

        rule = mapnik.Rule()
        rule.filter = mapnik.Expression(expression)
        rule.symbols.append(pt_symbolizer)
        mapnik_style.rules.append(rule)

    mapnik_style = mapnik.Style()

    symbol = legend["symbology"][0]
    min_threshold = symbol["value"]

    for index, symbol in enumerate(legend["symbology"][1:]):
        max_threshold = symbol["value"]
        expression = (
            f"[__variable__{variable}] < {max_threshold} and [__variable__{variable}]"
            f" >= {min_threshold}"
        )

        _add_rule(mapnik_style, expression, index)

        min_threshold = max_threshold

    expression = f"[__variable__{variable}] >= {min_threshold}"
    _add_rule(mapnik_style, expression, len(legend["symbology"]) - 1)

    return mapnik_style, "vector_point_style"
