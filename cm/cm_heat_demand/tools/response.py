import numpy as np


def get_response(
    total_potential: float, total_heat_demand: float, areas_potential: np.ndarray
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
        total_potential: float,
        total_heat_demand: float,
        areas_potential: np.ndarray,
    ) -> dict:
        """
        Add information about the graphics to the based dictionary.

        Inputs :
            * base_dictionary : dictionary that will be updated.
            * total_potential : total potential of all areas.
            * total_heat_demand : total demand of all areas.
            * areas_potential : potential of each area.
        Output :
            * base_dictionary : updated dictionary.
        """

        # Demand - Potential (GWh/year)
        base_dictionary["graphs"] = dict()
        base_dictionary["graphs"]["Potential"] = dict()
        base_dictionary["graphs"]["Potential"]["type"] = "bar"
        base_dictionary["graphs"]["Potential"]["values"] = [
            ["District heating potential", total_potential],
            ["Annual heat demand", total_heat_demand],
        ]

        # Areas potential
        base_dictionary["graphs"]["Areas potential"] = dict()
        base_dictionary["graphs"]["Areas potential"]["type"] = "bar"
        if areas_potential.size == 0:
            values = [
                ["Zone " + str(index + 1), value]
                for index, value in enumerate(areas_potential)
            ]
        else:
            values = [["Zone 1", 0.0]]
        base_dictionary["graphs"]["Areas potential"]["values"] = values

        base_dictionary["graphs"]["cm-heat-demand test graph"] = dict()
        base_dictionary["graphs"]["cm-heat-demand test graph"]["type"] = "xy"
        base_dictionary["graphs"]["cm-heat-demand test graph"]["values"] = [(i, i) for i in range(100)]

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
            "Total potential": total_potential,
            "Total heat demand": total_heat_demand,
        }

        return base_dictionary

    def get_geofiles(
        base_dictionary: dict,
        areas_path: str = "fake path to the geofile",
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
        base_dictionary["geofiles"]["areas"] = areas_path

        return base_dictionary

    response = dict()
    response = get_graphs(
        base_dictionary=response,
        total_potential=total_potential,
        total_heat_demand=total_heat_demand,
        areas_potential=areas_potential,
    )
    response = get_indicators(base_dictionary=response)
    response = get_geofiles(base_dictionary=response)

    return response
