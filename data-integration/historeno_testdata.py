import os

import geopandas as gpd
import sqlalchemy
from historeno_settings import DB_URL
import sqlalchemy as sqla
# from sqlalchemy import create_engine
from os.path import abspath, dirname, isfile, join, isdir

CURRENT_DIR = dirname(abspath(__file__))
DATA_DIR = join(CURRENT_DIR, "data")


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
    print(os.listdir(DATA_DIR))
    if not isfile(file):
        print("ddata-integration\data\sample_bat_fr.shp")
        raise FileExistsError(file)
    dataframe = gpd.read_file(filename=file)
    return dataframe


def post_data(
    data: gpd.GeoDataFrame,
    engine_: sqlalchemy.engine.Engine,
    table: str,
    **kwargs,
) -> None:
    data.to_postgis(
        table,
        engine_,
        if_exists="append",
        index=False,
        **kwargs,
    )


if __name__ == "__main__":
    engine = get_engine()
    geo_dataframe = read_data()
    post_data(data=geo_dataframe, engine_=engine, table="historeno_test")
    print("done")
