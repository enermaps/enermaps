from os import remove
from os.path import exists, isfile, join
from uuid import uuid1

from BaseCM.cm_output import validate
from tools import settings
from tools.areas import get_areas
from tools.geofile import clip_raster, get_projection, write_raster
from tools.response import get_response

from tempfile import TemporaryDirectory


def remove_files(*files):
    for file in files:
        assert exists(file) is True, "The file does not exist : {}".format(file)
        remove(file)


class IntervalError(Exception):
    """
    Exception thrown when value is not between a given interval.
    """
    pass


def is_between(value: float, min_value: float, max_value: float):
    if min_value <= value <= max_value:
        return True
    else:
        raise IntervalError(f"{value} not between {min_value} and {max_value}")
    

def processing(region: dict, raster: str, parameters: dict):
    is_between(value=parameters["pixel_threshold"], min_value=0, max_value=1000)
    is_between(value=parameters["district_heating_zone_threshold"], min_value=0, max_value=500)

    with TemporaryDirectory(dir=settings.TESTDATA_DIR) as temp_dir:

        clipped_raster = join(temp_dir, "raster_tmp.tif")
        clip_raster(src=raster, shapes=region, dst=clipped_raster)

        (
            geo_transform,
            total_heat_demand,
            areas,
            filtered_map,
            total_potential,
            areas_potential,
        ) = get_areas(
            heat_density_map=clipped_raster,
            pixel_threshold=parameters["pixel_threshold"],
            district_heating_zone_threshold=parameters["district_heating_zone_threshold"],
        )

        ouput_raster = join(temp_dir, "out.tif")
        write_raster(
            map_array=filtered_map,
            projection=get_projection(geofile=clipped_raster),
            geotransform=geo_transform,
            dst=ouput_raster,
        )

        response = get_response(
            total_potential=total_potential,
            total_heat_demand=total_heat_demand,
            areas_potential=areas_potential,
        )

        remove_files(clipped_raster, ouput_raster)

    validate(response)

    return response
