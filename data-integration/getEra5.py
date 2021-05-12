import argparse
import json
import logging
import os
import shutil
import sys

import cdsapi
import pandas as pd
import utilities
from pyproj import CRS

logging.basicConfig(level=logging.INFO)
EPSG = 4326
DT = 1  # hours per final file
LIMIT = 1  # number of days
YEARS_BACK = 5
AREA = [
    84.17,
    -24.8,  # -16.1 excludes Iceland
    32.88,
    40.18,
]  # North-West-South-East
DELETE_ORIG = True
c = cdsapi.Client()


VARIABLES = {
    "10m_u_component_of_wind": "u10",
    "10m_v_component_of_wind": "v10",
    "2m_dewpoint_temperature": "d2m",
    "2m_temperature": "t2m",
    "mean_sea_level_pressure": "msl",
    "mean_wave_direction": "mwd",
    "mean_wave_period": "mwp",
    "sea_surface_temperature": "sst",
    "significant_height_of_combined_wind_waves_and_swell": "swh",
    "surface_pressure": "sp",
    "total_precipitation": "tp",
}

# In Docker
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DB = os.environ.get("DB_DB")

DB_URL = "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
    DB_HOST=DB_HOST,
    DB_PORT=DB_PORT,
    DB_USER=DB_USER,
    DB_PASSWORD=DB_PASSWORD,
    DB_DB=DB_DB,
)


def prepare(dp: dict = None):
    """
    Prepare rasters.

    Parameters
    ----------
    dp : dict, optional
        meatadata (not a real dp). The default is None.

    Returns
    -------
    None.

    """
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    times = pd.date_range(dp["start_at"], dp["end_at"], freq="d")
    rasters = []
    for time in times[:LIMIT]:
        for variable in VARIABLES.keys():
            filename = str(time.date()) + "_" + VARIABLES[variable] + ".nc"
            if not os.path.exists(os.path.join("tmp", filename)):
                logging.info("Downloading {}".format(filename))
                c = cdsapi.Client()
                c.retrieve(
                    "reanalysis-era5-single-levels",
                    {
                        "product_type": "reanalysis",
                        "format": "netcdf",
                        "variable": variable,
                        "year": [time.year],
                        "month": [time.month],
                        "day": [str(d + 1).zfill(2) for d in range(time.days_in_month)],
                        "time": [str(d).zfill(2) + ":00" for d in range(24)],
                        "area": AREA,
                    },
                    os.path.join("tmp", filename),
                )
            raster = {
                "value": os.path.join("tmp", filename),
                "start_at": time,
                "z": None,
                "unit": None,
                "dt": DT,
                "crs": CRS.from_epsg(EPSG),
                "variable": VARIABLES[variable],
            }
            rasters.append(raster)
    rasters = pd.DataFrame(rasters)
    enermaps_data = utilities.prepareRaster(rasters, delete_orig=DELETE_ORIG)
    return enermaps_data


def get(url: str, dp: dict, force: bool = False):
    """
    Retrieve data and check update.

    Parameters
    ----------
    url : str
        URL to retrieve the data from.
    dp : dict
        metadata (not a real dp) against which validating the data.
    force : Boolean, optional
        If True, new data will be uploaded even if the same as in the db. The default is False.

    Returns
    -------
    DataFrame
        Data in EnerMaps format.
    dict
        metadata

    """
    end_year = pd.Timestamp.today().year - 1
    start_year = end_year - YEARS_BACK
    times = pd.date_range(
        "01-01-{}".format(start_year), "31-12-{}".format(end_year), freq="d"
    )

    new_dp = {"start_at": str(times[0]), "end_at": str(times[-1])}

    # Logic for update
    if dp is not None:  # Existing dataset
        # check stats
        isChanged = dp != new_dp
        if isChanged:  # Data integration will continue, regardless of force argument
            logging.info("Data has changed")
            enermaps_data = prepare(new_dp)
        elif force:  # Data integration will continue, even if data has not changed
            logging.info("Forced update")
            enermaps_data = prepare(new_dp)
        else:  # Data integration will stop here, returning Nones
            logging.info("Data has not changed. Use --force if you want to reupload.")
            return None, None
    else:  # New dataset
        enermaps_data = prepare(new_dp)

    return enermaps_data, new_dp


def postProcess(data: pd.DataFrame):
    """
    Coplete additional columns of the dataframe.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame in EnerMaps format.

    Returns
    -------
    data : pd.DataFrame
        DataFrame in EnerMaps format with completed fields.

    """
    # invert dict -> short_name: long_name
    variables = {v: k for k, v in VARIABLES.items()}
    for i, row in data.iterrows():
        fields = json.loads(row["fields"])
        data.loc[i, "unit"] = fields["units"]
    data["variable"] = data["variable"].replace(variables)
    return data


if __name__ == "__main__":
    datasets = pd.read_csv("datasets.csv", engine="python", index_col=[0])
    ds_ids = datasets[datasets["di_script"] == os.path.basename(sys.argv[0])].index
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Import HotMaps raster")
        parser.add_argument("--force", action="store_const", const=True, default=False)
        parser.add_argument(
            "--select_ds_ids", action="extend", nargs="+", type=int, default=[]
        )
        args = parser.parse_args()
        isForced = args.force
        if len(args.select_ds_ids) > 0:
            ds_ids = args.select_ds_ids
    else:
        isForced = False

    for ds_id in ds_ids:
        logging.info("Retrieving Dataset {}".format(ds_id))
        dp = utilities.getDataPackage(
            ds_id,
            "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}".format(
                DB_HOST=DB_HOST,
                DB_PORT=DB_PORT,
                DB_USER=DB_USER,
                DB_PASSWORD=DB_PASSWORD,
                DB_DB=DB_DB,
            ),
        )

        data, dp = get(datasets.loc[ds_id, "di_URL"], dp, isForced)

        if isinstance(data, pd.DataFrame):
            if utilities.datasetExists(ds_id, DB_URL,):
                utilities.removeDataset(ds_id, DB_URL)
                logging.info("Removed existing dataset")

            # Move rasters into the data directory
            if not os.path.exists("data"):
                os.mkdir("data")
            if not os.path.exists(os.path.join("data", str(ds_id))):
                os.mkdir(os.path.join("data", str(ds_id)))
            for i, row in data.iterrows():
                shutil.move(row.fid, os.path.join("data", str(ds_id), row.fid))

            # Postprocess
            data = postProcess(data)

            # Create dataset table
            metadata = datasets.loc[ds_id].fillna("").to_dict()
            metadata["datapackage"] = dp
            metadata = json.dumps(metadata)
            dataset = pd.DataFrame([{"ds_id": ds_id, "metadata": metadata}])
            utilities.toPostgreSQL(
                dataset, DB_URL, schema="datasets",
            )

            # Create data table
            data["ds_id"] = ds_id
            utilities.toPostgreSQL(
                data, DB_URL, schema="data",
            )

            # Create empty spatial table
            spatial = pd.DataFrame()
            spatial[["fid", "ds_id"]] = data[["fid", "ds_id"]]
            utilities.toPostgreSQL(
                spatial, DB_URL, schema="spatial",
            )
