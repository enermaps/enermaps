import numpy as np
from scipy.ndimage import binary_dilation, binary_erosion, measurements

from .geofile import read_raster


class MapSizeError(Exception):
    """Exception thrown for map size error."""

    pass


def get_browsing_indexes(
    labels_array: np.ndarray, pixel_filtered_map: np.ndarray, labels_number: int
):
    """
    This function :
        * find the row, the column, the label, the value of each non-null pixel in list,
        * sort this list based on the label and save it as numpy array,
        * and then calculate the indexes of the first and the last element of the sorted list
          that belongs to the same label.

    Afterwards, the sorted list will be browsed piece by piece
    (i.e. label by label) thanks to the indexes.

    Inputs :
        * labels_array : label map.
        * pixel_filtered_map : pixel filtered map.
        * labels_number : number of labels.

    Outputs :
        * end : list of index of the first element of given label.
        * start : list of index of the first element of given label.
        * sorted_array : array (1xn) sorted by labels of rows, columns,
                         labels, value of each non-null pixel.
    """
    if labels_array.shape != pixel_filtered_map.shape:
        raise MapSizeError("The maps used have not the same size.")

    rows, columns = np.nonzero(labels_array)
    labels = labels_array[rows, columns]
    district_heating = pixel_filtered_map[rows, columns]
    sorted_array = np.asarray(
        sorted(
            zip(rows, columns, labels, district_heating),
            key=lambda items: items[2],
        )
    )

    unique_items, counts = np.unique(labels, return_counts=True)
    end = np.cumsum(counts)
    start = np.concatenate(
        (
            np.zeros((1)),
            end[0 : labels_number - 1],
        )
    )

    return end.astype(int), start.astype(int), sorted_array


def define_areas(
    pixel_filtered_map: np.ndarray, district_heating_zone_threshold: float
):
    """
    This function defines areas where the sum of the pixel values for a given
    area exceeds a certain threshold.

    Inputs :
        * pixel_filtered_map : pixel filtered map (in MWh).
        * district_heating_zone_threshold : threshold that the areas must meet (in GWh/a).

    Outputs :
        * areas :
            - map where the value of the pixels belonging to a given area corresponds
            to the potential of this area.
        * filtered_map :
            - map where the values of the pixels not belonging to a filtered area
            are set to zero.
        * total_potential :
            - the sum of the potential of each zone.
        * areas_potential :
            - list of the potential of each zone.

            The pixels that do not pass the thresholds (and therefore defined with a potential equal to zero)
            belong to the first zone.
            For example : [0, "1st area potential", ..., "nth area potential"]
            - NB: this zone is not interesting, therefore only the potential of the other zones
                is returned in practice
    """
    structure = np.ones((3, 3)).astype(int)
    expanded_map = binary_dilation(input=pixel_filtered_map, structure=structure)
    eroded_map = binary_erosion(input=expanded_map, structure=structure)
    labels_array, labels_number = measurements.label(
        input=eroded_map,
        structure=structure,
    )

    if labels_array.size > 0:
        end, start, sorted_array = get_browsing_indexes(
            labels_array=labels_array,
            pixel_filtered_map=pixel_filtered_map,
            labels_number=labels_number,
        )

        # labels start from 1, therefore the array size is 'num_labels_array + 1'
        areas_potential = np.zeros((labels_number + 1)).astype(float)
        for i, (start_, end_) in enumerate(zip(start, end)):
            area = sorted_array[start_:end_, 3]
            area_potential = np.sum(area)
            if area_potential >= district_heating_zone_threshold:
                # i+1 because labeling starts from 1 and not from 0
                # factor 0.001 for conversion from MWh/ha to GWh/ha
                areas_potential[i + 1] = area_potential * 0.001

        areas = areas_potential[labels_array]

        filtered_map = pixel_filtered_map * (areas > 0).astype(int)
        total_potential = np.sum(areas_potential)

        return areas, filtered_map, total_potential, areas_potential[1:]
    else:
        # TODO :
        #  * manage when labels_array.size =< 0:
        return None


def get_areas(
    heat_density_map: str,
    pixel_threshold: float,
    district_heating_zone_threshold: float,
):
    """
    This function applies a filter on each individual pixel as well as on all the pixels belonging to the same area.

    These areas are defined by the set of adjacent pixels that have passed the first filter.

    Inputs :
        * heat_density_map : path to the clipped raster (in MWh).
        * pixel_threshold : threshold that each pixel must reach (in MWh).
        * district_heating_zone_threshold : threshold that each zone must reach (in GWh/a).

    Outputs :
        * areas :
            - map where the value of the pixels belonging to a given area corresponds
            to the potential of this area.
        * filtered_map :
            - map where the values of the pixels not belonging to a filtered area
            are set to zero.
        * total_potential :
            - sum of the potential of each zone.
        * total_heat_demand :
            - total heat demand of the map (in GWh)
        * areas_potential :
            - list of the potential of each zone.

            The pixels that do not pass the thresholds (and therefore defined with a potential equal to zero)
            belong to the first zone.
            For example : [0, "1st area potential", ..., "nth area potential"]
            - NB: this zone is not interesting, therefore only the potential of the other zones
                is returned in practice
    """
    array_map, geo_transform = read_raster(raster=heat_density_map)
    # array_map : MWh

    # factor 1000 for conversion from MWh to GWh
    total_heat_demand = np.around(np.sum(array_map) / 1000, 2)

    # pixel threshold filter
    pixel_filtered_map = array_map * (array_map > pixel_threshold)

    # factor 1000 for conversion from GWh/a to MWh/a
    district_heating_zone_threshold = district_heating_zone_threshold * 1000

    # district_heating_zone_threshold filter
    areas, filtered_map, total_potential, areas_potential = define_areas(
        pixel_filtered_map=pixel_filtered_map,
        district_heating_zone_threshold=district_heating_zone_threshold,
    )

    return (
        areas,
        geo_transform,
        areas_potential,
        filtered_map,
        total_potential,
        total_heat_demand,
    )
