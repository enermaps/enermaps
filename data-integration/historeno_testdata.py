import json
from os.path import abspath, dirname, isfile, join

import geopandas as gpd
import pandas as pd
import shapely
import sqlalchemy
import sqlalchemy as sqla

from historeno_settings import DB_URL

CURRENT_DIR = dirname(abspath(__file__))
DATA_DIR = join(CURRENT_DIR, "inputs")


def get_engine() -> sqlalchemy.engine.Engine:
    # DB_URL = "postgresql://postgres:postgres@localhost:5432/dataset"
    _engine = sqla.create_engine(url=DB_URL)
    print(f"DATA BASE URL : {DB_URL}")
    try:
        connection = _engine.connect()
        connection.close()
    except Exception:
        raise NotImplementedError
    return _engine


def read_data() -> gpd.GeoDataFrame:
    file = join(DATA_DIR, "datasets.shp")
    if not isfile(file):
        raise FileExistsError(file)
    dataframe = gpd.read_file(filename=file)
    return dataframe


def post_data(
    data: gpd.GeoDataFrame,
    engine_: sqlalchemy.engine.Engine,
    **kwargs,
) -> None:

    ds_id = 1

    # DATASETS TABLE
    d = {
        "ds_id": [ds_id],
        "metadata": [
            {
                "Title": "Sample of bulding",
                "parameters": {"is_raster": False, "is_tiled": False},
                "Group": "Building",
            }
        ],
        "share_id": ["building_share_id"],
    }
    datasets = pd.DataFrame(data=d)
    datasets["metadata"] = datasets["metadata"].apply(json.dumps)
    datasets.to_sql(
        "datasets",
        engine_,
        if_exists="append",
        index=False,
        **kwargs,
    )

    # SPATIAL TABLE
    spatial_data = data.copy(deep=True)
    spatial_data = spatial_data[["geometry"]]
    spatial_data["geometry"] = spatial_data["geometry"].apply(
        lambda shape: shapely.ops.transform(lambda x, y, z: (x, y), shape)
    )
    spatial_data["ds_id"] = [ds_id for fid in range(spatial_data.shape[0])]
    spatial_data["levl_code"] = ["geometry" for fid in range(spatial_data.shape[0])]
    spatial_data["cntr_code"] = [None for fid in range(spatial_data.shape[0])]
    spatial_data["name_engl"] = [None for fid in range(spatial_data.shape[0])]
    spatial_data["name"] = [None for fid in range(spatial_data.shape[0])]
    spatial_data["fid"] = [fid for fid in range(spatial_data.shape[0])]
    spatial_data.to_postgis(
        "spatial",
        engine_,
        if_exists="append",
        index=False,
        **kwargs,
    )

    # DATA TABLE
    rows = 10
    d = {
        "index": [ds_id ** (2**2 + _) for _ in range(rows)],
        "start_at": [None for _ in range(rows)],
        "fields": [None for _ in range(rows)],
        "variable": [None for _ in range(rows)],
        "unit": [None for _ in range(rows)],
        "value": [None for _ in range(rows)],
        "ds_id": [ds_id for _ in range(rows)],
        "fid": [None for _ in range(rows)],
        "dt": [None for _ in range(rows)],
        "z": [None for _ in range(rows)],
        "isRaster": [False for _ in range(rows)],
    }
    data_data = pd.DataFrame(data=d)
    data_data.to_sql(
        "data",
        engine_,
        if_exists="append",
        index=False,
        **kwargs,
    )


if __name__ == "__main__":
    engine = get_engine()
    geo_dataframe = read_data()
    post_data(data=geo_dataframe, engine_=engine)
    print("done")
