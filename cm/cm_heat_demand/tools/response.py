import logging

import jenkspy
import numpy as np
from matplotlib import cm as colormap


def get_response(
    map_array: np.ndarray,
    total_potential: float,
    total_heat_demand: float,
    areas_potential: np.ndarray,
    raster_name: str,
) -> dict:
    """
    Generate the the dictionary return by the CM.

    Inputs :
        * total_potential : total potential of all areas.
        * total_heat_demand : total demand of all areas.
        * areas_potential : potential of each area.

    Output :
        * response : dictionary that will be sent by the CM.
    """

    def get_graphs(
        base_dictionary: dict,
        areas_potential: np.ndarray,
    ) -> dict:
        """
        Add information about the graphics to the based dictionary.

        Inputs :
            * base_dictionary : dictionary that will be updated.
            * areas_potential : potential of each area.
        Output :
            * base_dictionary : updated dictionary.
        """

        base_dictionary["graphs"] = dict()

        # Areas potential
        if areas_potential.size > 0:
            base_dictionary["graphs"] = list()
            base_dictionary["graphs"].append(dict())
            base_dictionary["graphs"][0]["Areas potentials (GWh)"] = dict()
            base_dictionary["graphs"][0]["Areas potentials (GWh)"]["type"] = "bar"

            generator = [element for element in areas_potential if element > 0]
            generator.sort(reverse=True)
            values = [
                ("Zone " + str(index + 1), value)
                for index, value in enumerate(generator)
            ]

            base_dictionary["graphs"][0]["Areas potentials (GWh)"]["values"] = values

        return base_dictionary

    def get_indicators(base_dictionary: dict) -> dict:
        """
        Add information about the indicators to the based dictionary.

        Inputs :
            * base_dictionary : dictionary that will be updated.

        Output :
            * base_dictionary : updated dictionary.
        """

        base_dictionary["values"] = {
            "Total district heating potential (GWh)": round(total_potential, 2),
            "Total heat demand (GWh)": round(total_heat_demand, 2),
            "Potential share of district heating from total "
            "demand in selected zone (%)": round(
                total_potential / total_heat_demand * 100, 2
            ),
        }

        return base_dictionary

    def get_geofiles(
        base_dictionary: dict,
        layer_name: str,
    ) -> dict:
        """
        Add path towards the geofiles to the based dictionary.

        Inputs :
            * base_dictionary : dictionary that will be updated.
            * areas_path : path to the areas  geofile.

        Output :
            * base_dictionary : updated dictionary.
        """

        base_dictionary["geofiles"] = dict()
        base_dictionary["geofiles"]["areas"] = layer_name

        return base_dictionary

    def get_legend(
        map_array: np.array,
        base_dictionary: dict,
        legend_name: str = "Heat demand",
        unit: str = "MWh",
        nb_class: int = 5,
        colormap_name: str = "plasma",
    ) -> dict:
        """Prepare a legend dict in HotMaps format"""
        if not isinstance(nb_class, int):
            raise TypeError(f"{nb_class} type is not 'int'.")
        if not isinstance(colormap_name, str):
            raise TypeError(f"{colormap_name} type is not 'str'.")
        if not isinstance(legend_name, str):
            raise TypeError(f"{legend_name} type is not 'str'")
        listify_array = map_array[~np.isnan(map_array)]
        listify_array = np.unique(listify_array)
        nb_class = min([nb_class, listify_array.shape[0] - 1])
        if nb_class > 2:
            color_scale = colormap.get_cmap(name=colormap_name, lut=nb_class).colors
            color_scale[:, :-1] *= 255
            breaks = jenkspy.jenks_breaks(listify_array, nb_class=nb_class)
            logging.info("=== BREAKS ===")
            logging.error(breaks)
            logging.error(listify_array)
            legend = {"name": legend_name, "type": "custom", "symbology": []}
            for enum, i in enumerate(range(len(breaks) - 1)):
                legend["symbology"].append(
                    {
                        "red": float(color_scale[i, 0]),
                        "green": float(color_scale[i, 1]),
                        "blue": float(color_scale[i, 2]),
                        "opacity": float(color_scale[i, 3]),
                        "value": float(breaks[i]),
                        "label": "≥ {} {}".format(int(round(breaks[i], 0)), unit),
                    }
                )
                # if enum == 0:
                #     legend["symbology"][0]["value"] = 1**-6
        else:
            legend = {}
            print("No legend was created.", flush=True)
        base_dictionary["legend"] = legend
        return base_dictionary

    response = dict()
    response = get_graphs(base_dictionary=response, areas_potential=areas_potential)
    response = get_indicators(base_dictionary=response)
    response = get_geofiles(base_dictionary=response, layer_name=raster_name)
    response = get_legend(base_dictionary=response, map_array=map_array)

    return response
