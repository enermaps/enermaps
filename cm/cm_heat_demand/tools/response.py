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
        if areas_potential[1:].size > 0:
            print("areas_potential")
            print(areas_potential[1:])
            base_dictionary["graphs"]["Areas potentials (GWh)"] = dict()
            base_dictionary["graphs"]["Areas potentials (GWh)"]["type"] = "bar"

            # labels start from 1, therefore the array size is 'num_labels_array + 1'
            generator = [element for element in areas_potential[1:] if element > 0]

            values = [
                ("Zone " + str(index + 1), value)
                for index, value in enumerate(generator)
            ]

            base_dictionary["graphs"]["Areas potentials (GWh)"]["values"] = values

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
    response = get_graphs(base_dictionary=response, areas_potential=areas_potential)
    response = get_indicators(base_dictionary=response)
    response = get_geofiles(base_dictionary=response)

    return response
