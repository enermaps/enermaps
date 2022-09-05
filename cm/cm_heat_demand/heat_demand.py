from os.path import join
from tempfile import TemporaryDirectory

from BaseCM.cm_output import validate
from BaseCM.cm_raster import clip_raster, get_projection, write_raster

from tools import settings
from tools.areas import get_areas
from tools.response import get_response


def processing(task, region: dict, raster: str, parameters: dict):
    """
    Cuts the raster according to given region and applies some filters
    in order to find the district heating potentials and
    related indicators.


    Inputs :
        * region : selected zone where the district heating potential is studied.
        * raster : raster of the heat demand.
        * parameters : the pixel and area thresholds.

    Output :
        * Indicators :
        * Graphics : Potential of areas that pass the filters.
        * Layer : Areas that pass the filters.
    """

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
            pixel_threshold=parameters["Heat demand in hectare (MWh/ha)"],
            district_heating_zone_threshold=parameters[
                "Heat demand in a DH zone (GWh/year)"
            ],
        )

        dst_raster = join(temp_dir, "dst.tif")
        write_raster(
            map_array=filtered_map,
            projection=get_projection(geofile=clipped_raster),
            geotransform=geo_transform,
            dst=dst_raster,
        )

        raster_name = "areas.tif"

        response = get_response(
            map_array=filtered_map,
            total_potential=total_potential,
            total_heat_demand=total_heat_demand,
            areas_potential=areas_potential,
            raster_name=raster_name,
        )

        with open(dst_raster, mode="rb") as raster_fd:
            task.post_raster(raster_name=raster_name, raster_fd=raster_fd)

    validate(response)

    return response
