"""Functions related to the "GetMap" operation of the Web Map Service (WMS)"""

import mapnik

from app.common import path
from app.data_integration import data_endpoints
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

    # Get the list of the layers to display
    layers = utils.parse_layers(normalized_args)
    for layer_name in layers:
        layer = geofile.load(layer_name)
        if layer is None:
            return None

        mapnik_layers = layer.as_mapnik_layers()
        if mapnik_layers is None:
            return None

        if path.get_type(layer_name) in (path.RASTER, path.VECTOR):
            (legend_style, legend_style_name) = create_style_from_legend(
                layer_name, layer, mapnik_layers[0]
            )
        else:
            create_default_style()
            legend_style = None

        if legend_style is not None:
            mp.append_style(legend_style_name, legend_style)

        for mapnik_layer in mapnik_layers:
            mapnik_layer.styles.append(line_style_name)

            if legend_style is not None:
                mapnik_layer.styles.append(legend_style_name)

            mp.layers.append(mapnik_layer)

    return mp


def create_style_from_legend(layer_name, layer, mapnik_layer):
    # return (None, None)

    (type, layer_id, variable, _) = path.parse_unique_layer_name(layer_name)

    # Get the layer style and type
    legend_style = data_endpoints.get_legend_style(layer_id)
    layer_type, data_type = data_endpoints.get_ds_type(layer_id)

    mapnik_style = None
    style_name = None

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
            mapnik_style, style_name = make_numerical_polygon_style(
                variable, legend_style
            )
        else:
            legend_images = layer.get_legend_images(legend_style)
            mapnik_style, style_name = make_numerical_point_style(
                variable, legend_style, legend_images
            )

    elif type == path.RASTER:
        if data_type == "numerical":
            mapnik_style, style_name = make_numerical_raster_style(legend_style)
        elif data_type == "categorical":
            mapnik_style, style_name = make_categorical_raster_style(legend_style)

    return (mapnik_style, style_name)


def create_default_style():
    #     # Make a default numerical raster layer style (the layer should be a
    #     # raster layer produced by a CM)
    #     legend_style = []
    #     min_value = 0
    #     max_value = 255
    #     color = (1, 0, 0)  # Default red
    #     nb_of_colors = 8
    #     import seaborn as sns
    #
    #     color_list = sns.dark_palette(color, n_colors=nb_of_colors, input="rgb")
    #     color_list = [
    #         (
    #             (int(255 * color[0])),
    #             (int(255 * color[1])),
    #             (int(255 * color[2])),
    #         )
    #         for color in color_list
    #     ]
    #     for n, color in enumerate(color_list, start=1):
    #         min_threshold = min_value + (n - 1) * (
    #             (max_value - min_value) / nb_of_colors
    #         )
    #         min_threshold = round(min_threshold, 2)
    #         max_threshold = min_value + n * (
    #             (max_value - min_value) / nb_of_colors
    #         )
    #         max_threshold = round(max_threshold, 2)
    #         legend_style.append((color, min_threshold, max_threshold))
    #     mapnik_style, style_name = make_numerical_raster_style(legend_style)
    #     mapnik_layer.styles.append(style_name)
    #     mp.append_style(style_name, mapnik_style)
    pass


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


def make_numerical_raster_style(layer_style):
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
    for n, (color, min_threshold, max_threshold) in enumerate(layer_style):
        raster_colorizer.add_stop(
            max_threshold, mapnik.COLORIZER_LINEAR, mapnik.Color(*color)
        )

    raster_symb.colorizer = raster_colorizer
    rule.symbols.append(raster_symb)
    mapnik_style.rules.append(rule)
    return mapnik_style, "num_raster_style"


def make_categorical_raster_style(layer_style):
    """
    Make a style for categorical rasters.
    """
    mapnik_style = mapnik.Style()
    rule = mapnik.Rule()

    raster_symb = mapnik.RasterSymbolizer()
    raster_symb.colorizer = mapnik.RasterColorizer(
        mapnik.COLORIZER_LINEAR, mapnik.Color("transparent")
    )

    for n, (color_id, color) in enumerate(layer_style):
        raster_symb.colorizer.add_stop(color_id, mapnik.Color(*(color[0])))

    rule.symbols.append(raster_symb)
    mapnik_style.rules.append(rule)
    return mapnik_style, "categorical_raster_style"


def make_numerical_polygon_style(variable, layer_style):
    """
    Make a style for vector polygons
    """
    mapnik_style = mapnik.Style()
    nb_of_colors = len(layer_style)
    for n, (color, min_threshold, max_threshold) in enumerate(layer_style):
        if n == 0:
            expression = f"[__variable__{variable}] < {max_threshold}"
        elif n == nb_of_colors - 1:
            expression = f"[__variable__{variable}] >= {min_threshold}"
        else:
            expression = f"[__variable__{variable}] < {max_threshold} and [__variable__{variable}] >= {min_threshold}"

        polygon_symb = mapnik.PolygonSymbolizer()
        polygon_symb.fill = mapnik.Color(*color)
        polygon_symb.fill_opacity = 0.5

        rule = mapnik.Rule()
        rule.filter = mapnik.Expression(expression)
        rule.symbols.append(polygon_symb)
        mapnik_style.rules.append(rule)
    return mapnik_style, "vector_polygon_style"


def make_numerical_point_style(variable, layer_style, legend_images):
    """
    Make a style for vector points
    """
    mapnik_style = mapnik.Style()
    nb_of_colors = len(layer_style)
    for n, (color, min_threshold, max_threshold) in enumerate(layer_style):
        if n == 0:
            expression = f"[__variable__{variable}] < {max_threshold}"
        elif n == nb_of_colors - 1:
            expression = f"[__variable__{variable}] >= {min_threshold}"
        else:
            expression = f"[__variable__{variable}] < {max_threshold} and [__variable__{variable}] >= {min_threshold}"

        pt_symbolizer = mapnik.PointSymbolizer()
        pt_symbolizer.file = legend_images[n]

        rule = mapnik.Rule()
        rule.filter = mapnik.Expression(expression)
        rule.symbols.append(pt_symbolizer)
        mapnik_style.rules.append(rule)

    return mapnik_style, "vector_point_style"
