import os
import argparse
import json
import sys
import utilities
import logging
from frictionless import Package, validate_package
from pandas_datapackage_reader import read_datapackage

import geopandas as gpd
import pandas as pd

#Constants

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

logging.basicConfig(level=logging.INFO)

NAME = "jrc-hydro-power-plant-database"

UNPIVOTING_FIELDS = ['installed_capacity_MW',
                     'pumping_MW',
                     'storage_capacity_MWh',
                     'avg_annual_generation_GWh']


def get(path, name):
    """
    Retrieves a datapackge and if valid transforms the data
    to match EnerMaps schema

    Parameters
    ----------
    path : str
        Path to the datapackage directory.
    name : str
        Name of the dataset.

    Returns
    -------
    enermaps_data : DataFrame
        DESCRIPTION.
    spatial : GeoDataFrame
        DESCRIPTION.

    """
    name = name.replace(" ","_") #make sure the name is without spaced
    path += "datapackage.json"
    val = validate_package(path)
    if val["valid"]:
        # Transform with pandas and geopandas
        data = read_datapackage(path)
        
        # Create unique id
        data["fid"] = name + "_" + data["id"]
        data.set_index("fid",inplace=True)
    
        spatial = gpd.GeoDataFrame(
            data.index,
            geometry=gpd.points_from_xy(data.lon, data.lat),
            crs="EPSG:4326"
        )
        spatial = spatial.to_crs("EPSG:3035")
        enermaps_data = data.melt(id_vars = data.columns[~data.columns.isin(UNPIVOTING_FIELDS)],
                        value_vars=UNPIVOTING_FIELDS,
                         ignore_index=False)
        enermaps_data["fields"] = enermaps_data[data.columns[~data.columns.isin(UNPIVOTING_FIELDS)]].to_dict(orient="records")
        enermaps_data["fields"] =  enermaps_data["fields"].apply(lambda  x: json.dumps(x))
        enermaps_data = enermaps_data.drop(data.columns[~data.columns.isin(UNPIVOTING_FIELDS)],axis=1)
        enermaps_data = pd.merge(enermaps_data,data, on="fid")
        enermaps_data["fields"] =  enermaps_data["fields"].apply(lambda  x: json.dumps(x))
        enermaps_data = enermaps_data.drop(data.columns,axis=1,errors="ignore")
        enermaps_data["unit"] = enermaps_data.variable.apply(lambda x: x.split("_")[-1])
        enermaps_data.reset_index(inplace=True)

        return enermaps_data, spatial
    else:
        print("Validation error")
        print(val)


if __name__ == '__main__':
    datasets = pd.read_csv("datasets.csv", engine="python", index_col=[0])
    ds_ids = datasets[datasets["di_script"] == os.path.basename(sys.argv[0])].index
    isForced = False
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Import Eurostat")
        parser.add_argument("--force", action="store_const", const=True, default=False)
        parser.add_argument(
            "--select_ds_ids", action="extend", nargs="+", type=int, default=[]
        )
        args = parser.parse_args()
        isForced = args.force
        if len(args.select_ds_ids) > 0:
            ds_ids = args.select_ds_ids
        

    for ds_id in ds_ids:
        logging.info("Processing ds {} - {}".format(ds_id, datasets.loc[ds_id,"Title (with Hyperlink)"]))

        if utilities.datasetExists(ds_id, DB_URL,):
                if isForced:
                    utilities.removeDataset(ds_id, DB_URL)
                    logging.info("Removed existing dataset")
                else:
                    logging.error("Dataset already existing. Use --force to replace it.")
    
        data, spatial = get(datasets.loc[ds_id, "di_URL"], NAME)
        
        dataset = pd.DataFrame([{"ds_id": ds_id, "metadata":datasets.loc[ds_id].to_json()}])
        utilities.toPostgreSQL(dataset,DB_URL, schema="datasets")
        
    
        data["ds_id"] =  ds_id
        utilities.toPostgreSQL(data,DB_URL, schema="data")
    
        
        spatial["ds_id"] =  ds_id
        utilities.toPostGIS(spatial,DB_URL, schema="spatial")
    

    
    