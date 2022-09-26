import json
from os.path import abspath, dirname, isfile, join

import geopandas as gpd
import pandas as pd
import shapely
import sqlalchemy

from settings import DB_URL

CURRENT_DIR = dirname(abspath(__file__))
DATA_DIR = join(CURRENT_DIR, "inputs")


def get_engine() -> sqlalchemy.engine.Engine:
    # DB_URL = "postgresql://postgres:postgres@localhost:5432/dataset"
    _engine = sqlalchemy.create_engine(url=DB_URL)
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
                "Group": "Bâtiment",
                "Title": "Bâtiments protégés",
                "parameters": {
                    "end_at": "2015-12-31 23:00",
                    "fields": [],
                    "levels": [],  # mandatory
                    "is_raster": False,
                    "start_at": "2021-06-30 12:00:00",
                    "is_tiled": False,
                    "variables": ["SRE"],  # mandatory
                    "time_periods": [],  # mandatory
                    "temporal_granularity": "hour",
                },
            }
        ],
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
    spatial_data["ds_id"] = [ds_id for _ in range(spatial_data.shape[0])]
    spatial_data["fid"] = [f"FR_{fid}" for fid in range(spatial_data.shape[0])]
    spatial_data["levl_code"] = ["geometry" for fid in range(spatial_data.shape[0])]
    spatial_data["cntr_code"] = [None for _ in range(spatial_data.shape[0])]
    spatial_data["name_engl"] = [None for _ in range(spatial_data.shape[0])]
    spatial_data["name"] = [None for _ in range(spatial_data.shape[0])]

    spatial_data.to_postgis(
        "spatial",
        engine_,
        if_exists="append",
        index=False,
        **kwargs,
    )

    # DATA TABLE
    rows = spatial_data.shape[0]
    fields = [
        {
            "Besoin": str(sre) + " kWh",
            "Demande": str(sre) + " kWh",
            "Pays": "France",
            "Region": "Jura-FR",
            "Altitude": 1000,
            "Météo": "Jura",
            "Context": "Urban",
            "Empreinte au sol": "[[0,0],[0,10],[10,10],[10,0]]",
            "Mitoyenneté": "[0,0,0.5,0]",
            "Typologie": 3,
            "Années de construction": 1950,
            "Catégorie d'ouvrage": 4,
            "Hauteur du bâtiment": 6,
            "Type de chauffage": "Pellets",
            "Année d'installation du chauffage": 1950,
            "Type d'émetteurs": "Murs chauffants",
            "Régulation du chauffage": "autre (+2°C)",
            "Isolation des conduites de chauffage": "Non isolées",
            "Isolation des conduites d'ECS": "Non isolées",
            "Présence d'une installation solaire thermique": "Oui",
            "Surface de capteurs solaires thermiques automatique": "Oui",
            "Surface de capteurs solaires thermiques": "Oui",
            "Nombre de logements": 10,
            "Efficacité des appareils électriques": "Meilleurs appareils",
            "Présence d'une ventilation mécanique": "Double flux",
            "Présence d'ascenseur(s)": "Simple flux",
            "Présence d'une instalaltion solaire PV": "Oui",
            "Surface PV automatique": "Oui",
            "Surface PV": "5",
            "Orientation PV": "70",
            "Présence de batteries de stockage": "Oui",
            "Note de protection du patrimoine": 10,
            "Possibilité d'utiliser un chauffage au bois": "Oui",
            "Possibilité de mettre des sondes géothermiques": "Oui",
            "Possibilité de mettre du solaire en toiture": "Oui",
        }
        for sre in range(rows)
    ]

    d = {
        "index": [index for index in range(rows)],
        "ds_id": [ds_id for _ in range(rows)],
        "fid": [f"FR_{fid}" for fid in range(rows)],
        "variable": ["SRE" for _ in range(rows)],
        "value": [value for value in range(rows)],
        "unit": ["m2" for _ in range(rows)],
        "start_at": ["2022-06-30 12:00:00" for _ in range(rows)],
        "fields": fields,
        "dt": [None for _ in range(rows)],
        "z": [None for _ in range(rows)],
        "israster": [False for _ in range(rows)],
    }
    data_data = pd.DataFrame(data=d)
    data_data["fields"] = data_data["fields"].apply(json.dumps)
    data_data.to_sql(
        "data",
        engine_,
        if_exists="append",
        index=False,
        **kwargs,
    )
