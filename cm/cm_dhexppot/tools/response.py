import logging

import jenkspy
import numpy as np
from matplotlib import cm as colormap


def get_response(
    P,
    result_dict,
    raster_name,
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
            base_dictionary["graphs"]["Areas potentials (GWh)"] = dict()
            base_dictionary["graphs"]["Areas potentials (GWh)"]["type"] = "bar"

            generator = [element for element in areas_potential if element > 0]
            generator.sort(reverse=True)
            values = [
                ("Zone " + str(index + 1), value)
                for index, value in enumerate(generator)
            ]

            base_dictionary["graphs"]["Areas potentials (GWh)"]["values"] = values

        return base_dictionary

    def get_indicators(base_dictionary, P, result_dict) -> dict:
        """
        Add information about the indicators to the based dictionary.

        Inputs :
            * base_dictionary : dictionary that will be updated.

        Output :
            * base_dictionary : updated dictionary.
        """
        
        if np.sum(
                            result_dict["supplied_heat_over_investment_period [TWh]"]
                        ) > 0:
                        
            ave_dh_grid_costs = np.round_(
                        (
                            np.sum(result_dict["gridCost [MEUR]"])
                            / np.sum(
                                result_dict["supplied_heat_over_investment_period [TWh]"]
                            )
                        ),
                        2,
                    )
        else:
            ave_dh_grid_costs = 0

        base_dictionary["values"] = {
            "Starting connection rate (%)": 100 * P.st_dh_connection_rate,
            "End connection rate (%)": 100 * P.end_dh_connection_rate,
            "Grid cost ceiling (EUR/MWh)": P.distribution_grid_cost_ceiling,
            "Start year - Heat demand in DH areas (GWh)": round(
                float(np.sum(result_dict["demand_st [GWh]"])), 1
            ),
            "End year - Heat demand in areas (GWh)": round(
                float(np.sum(result_dict["demand_end [GWh]"])), 1
            ),
            "Start year - Heat coverage by DH areas (GWh)": round(
                float(np.sum(result_dict["dhPot_%s [GWh]" % P.start_year])), 1
            ),
            "End year - Heat coverage by DH areas (GWh)": round(
                float(np.sum(result_dict["dhPot_%s [GWh]" % P.last_year])), 1
            ),
            "Total supplied heat by DH over the investment period (TWh)": round(
                float(
                    np.sum(result_dict["supplied_heat_over_investment_period [TWh]"])
                ),
                1,
            ),
            "Average DH grid cost in DH areas (EUR/MWh)": float(
                ave_dh_grid_costs
            ),
            "Total DH distribution grid length (km)": round(
                float(np.sum(result_dict["trench_len_dist [km]"])), 1
            ),
            "Total DH service pipe length (km)": round(
                float(np.sum(result_dict["trench_len_serv [km]"])), 1
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
        base_dictionary["geofiles"]["file"] = layer_name

        return base_dictionary

    def get_legend(
        base_dictionary: dict,
        leg_dict: dict,
        colormap_name: str = "viridis",
    ) -> dict:
        """Prepare a legend dict in HotMaps format"""
        legend_name = leg_dict["legend_name"]
        unit = leg_dict["unit"]
        nb_class = leg_dict["nb_class"]
        if not isinstance(nb_class, int):
            raise TypeError(f"{nb_class} type is not 'int'.")
        if not isinstance(colormap_name, str):
            raise TypeError(f"{colormap_name} type is not 'str'.")
        if not isinstance(legend_name, str):
            raise TypeError(f"{legend_name} type is not 'str'")
        # listify_array = map_array_leg[~np.isnan(map_array_leg)]
        # listify_array = np.unique(listify_array)
        # nb_class = min([nb_class, listify_array.shape[0] - 1])
        legend = {"name": legend_name, "type": "custom", "symbology": []}
        if nb_class == 5:
            listify_array = np.array([0, 15, 22, 29, 35, 50]).astype(int)
            color_scale = colormap.get_cmap(name=colormap_name, lut=nb_class).colors
            color_scale[:, :-1] *= 255
            breaks = jenkspy.jenks_breaks(listify_array, nb_class=nb_class)
            logging.info("=== BREAKS ===")
            logging.error(breaks)
            logging.error(listify_array)
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
        elif nb_class == 2:
            legend["symbology"] = legend["symbology"] + [
                {
                    "red": 222,
                    "green": 235,
                    "blue": 247,
                    "opacity": float(0.8),
                    "value": 0,
                    "label": "0 := No DH area",
                },
                {
                    "red": 49,
                    "green": 130,
                    "blue": 189,
                    "opacity": float(0.8),
                    "value": 1,
                    "label": "1 := Potential DH area",
                },
            ]
        else:
            legend = {}
            print("No legend was created.", flush=True)
        base_dictionary["legend"] = legend
        return base_dictionary

    legend_dict = {
        "Specific network costs": {
            "legend_name": "Network Costs",
            "unit": "EUR/MWh",
            "nb_class": 5,
        },
        "Potential district heating areas": {
            "legend_name": "Potential DH areas",
            "unit": "-",
            "nb_class": 2,
        },
    }
    response = dict()
    # response = get_graphs(response, areas_potential)
    response["graphs"] = []
    response = get_indicators(response, P, result_dict)
    if np.sum(result_dict["supplied_heat_over_investment_period [TWh]"]) > 0:
        response = get_geofiles(response, raster_name)
        response = get_legend(response, legend_dict[P.output_layer_selection])
    else:
        response["geofiles"] = dict()
        #response["legend"] = dict()
        
    return response
