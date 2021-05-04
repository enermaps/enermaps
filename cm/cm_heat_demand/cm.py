from os import remove
from os.path import exists, isfile, join
from uuid import uuid1

from BaseCM.cm_output import validate
from tools import settings
from tools.areas import get_areas
from tools.geofile import clip_raster, get_projection, write_raster
from tools.response import get_response


def random_filename(extension: str = ""):
    return str(uuid1()) + extension


def create_tmp_file(directory: str, filename: str, inplace: bool = True):
    file = join(directory, filename)
    if inplace and isfile(file):
        remove(file)
    return file


def remove_files(*files):
    for file in files:
        assert exists(file) is True, "The file does not exist : {}".format(file)
        remove(file)


def processing(region: dict, raster: str, parameters: dict):

    clipped_raster = create_tmp_file(
        directory=settings.TESTDATA_DIR,
        filename="raster_tmp.tif",
    )

    clip_raster(src=raster, shapes=region, dst=clipped_raster)

    (
        areas,
        geo_transform,
        areas_potential,
        filtered_map,
        total_potential,
        total_heat_demand,
    ) = get_areas(
        heat_density_map=clipped_raster,
        pixel_threshold=parameters["pixel_threshold"],
        district_heating_zone_threshold=parameters["district_heating_zone_threshold"],
    )

    ouput_raster = join(settings.TESTDATA_DIR, "out.tif")
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
