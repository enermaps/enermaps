#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging as log
import os
import sys
import tarfile
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
import pyproj
import rasterio
import urllib3

logging = log.getLogger("cm-hdd_cdd")
logging.setLevel(log.DEBUG)

DECIMALS = 3
CURRENT_FILE_DIR = Path(__file__).parent
TESTDATA_DIR = CURRENT_FILE_DIR / "testdata" / "hddcddrepo"


def get_data_dir() -> Path:
    return Path(os.environ["CM_HDD_CDD_DIR"])


def get_data_repository() -> Path:
    return Path(os.environ["CM_HDD_CDD_REPOSITORY"])


def get_years() -> List[int]:
    repo = get_data_repository()
    return sorted(set([int(gtif.name.split("_")[0]) for gtif in repo.glob("**/*.tif")]))


def get_scenarios() -> List[str]:
    repo = get_data_repository()
    return sorted([scn.name for scn in repo.iterdir()])


def get_base_temperature(ddtype: str) -> List[str]:
    repo = get_data_repository()
    folder = repo / "historical" / ddtype
    return sorted([float(tb.name) for tb in folder.iterdir()])


def get_hddcdd_schema(save: bool = False, schema_path: Path = None) -> Dict[str, Any]:
    scenarios = get_scenarios()
    scens = dict(
        type="string",
        title="Representative Concentration Pathway Scenarios",
        description=(
            "A Representative Concentration"
            " Pathway(https://en.wikipedia.org/wiki/Representative_Concentration_Pathway)"
            " (RCP) is a greenhouse gas concentration (not emissions) trajectory"
            " adopted by the IPCC"
        ),
        default=scenarios[0],
        enum=scenarios,
    )
    htemps = get_base_temperature("hdd")
    htemp = dict(
        type="number",
        title="Base temperature for HDD",
        description="",
        default=htemps[int(len(htemps) / 2)],
        minimum=min(htemps),
        maximum=max(htemps),
        enum=htemps,
    )
    ctemps = get_base_temperature("cdd")
    ctemp = dict(
        type="number",
        title="Base temperature for CDD",
        description="",
        default=ctemps[int(len(ctemps) / 2)],
        minimum=min(ctemps),
        maximum=max(ctemps),
        enum=ctemps,
    )
    props = {
        # "reference year": refyr,
        "scenario RCP": scens,
        "base temperature for HDD": htemp,
        "base temperature for CDD": ctemp,
    }
    schema = dict(type="object", properties=props)

    if save is True:
        if schema_path is None:
            cmpath = CURRENT_FILE_DIR.parent.parent.resolve()
            schema_path = cmpath / "hdd_cdd" / "schema.json"

        with open(schema_path.as_posix(), mode="w") as schfile:
            json.dump(schema, schfile, indent=2, sort_keys=True)
    return schema


def download_data():
    """Download HDDS and CDDs data.

    The function use the environmental variables:
    * `CM_HDD_CDD_REPOSITORY`
    * `INPUT_DATA_DIR`

    to define the path to the data repository.
    """
    rdir = get_data_dir()
    repo = get_data_repository()
    print(f"data repository => {repo}")
    os.makedirs(rdir.as_posix(), exist_ok=True)

    hist = repo / "historical"
    if hist.exists():
        print(
            f"The directory {hist} already exists, the dataset is not going to be"
            " downloaded."
        )
    else:
        print("Downloading the HDDs and CDDs dataset")
        url = "https://gitlab.inf.unibz.it/URS/enermaps/hdd-cdd/-/archive/main/hdd-cdd-main.tar.gz"
        zpath = rdir / "hdd-cdd-main.tar.gz"
        http = urllib3.PoolManager()
        with http.request("GET", url, preload_content=False) as req, open(
            zpath, "b+w"
        ) as zdata:
            zdata.write(req.read())
        print(f"Extracting {zpath}")
        with tarfile.open(zpath) as zfile:
            zfile.extractall(rdir)
        os.remove(zpath)
    print("done!")
    sys.exit(0)


def compute_centroid(geo) -> Tuple[float, float]:
    """
    Example
    >>> gj = {'features': [
    ...          {'geometry':
    ...               {'coordinates': [[[11.061588, 45.567844],
    ...                                 [11.055015, 45.563899],
    ...                                 [11.050421, 45.565349],
    ...                                 [11.040453, 45.560869],
    ...                                 [11.032734, 45.561389]]],
    ...                'type': 'Polygon'},
    ...           'id': 80284,
    ...           'properties': {'ds_id': 0,
    ...                          'dt': '',
    ...                          'fields': '',
    ...                          'id': 'IT_023038',
    ...                          'layer': '{ "type": "numerical" }',
    ...                          'start_at': '',
    ...                          'units': '{ "": null }',
    ...                          'variables': '{ "": 0 }',
    ...                          'z': ''},
    ...           'type': 'Feature'}],
    ...       'type': 'FeatureCollection'}
    >>> import geopandas as gpd
    >>> geo = gpd.GeoDataFrame.from_features(
    ...     gj["features"], crs="EPSG:4326"
    ... ).geometry
    >>> compute_centroid(geo)
    (11.048, 45.564)
    """
    # logging.warning(geo)
    try:
        coords = np.array(geo.to_crs("EPSG:3035").centroid.to_crs("EPSG:4326")[0])
    except KeyError:
        logging.error(geo)
        raise ValueError(
            "FAILED! The provided geometry is not a correct/supported geojson format."
        )
    return tuple(np.around(coords, decimals=DECIMALS))


def get_datarepodir() -> Path:
    return Path(os.environ.get("CM_HDD_CDD_REPOSITORY", TESTDATA_DIR.as_posix()))


@lru_cache(maxsize=256)
def get_datadir(
    datarepository: Path,
    sim_type: str = "historical",
    dd_type: str = "hdd",
    Tb=18.0,
    aggr_window="monthly",
    method="average",
) -> Path:
    """
    >>> get_datadir("cm/cm_hdd_cdd/testdata").as_posix()
    "cm/cm_hdd_cdd/testdata/historical/hdd/18.0/monthly/average/"
    """
    return (
        Path(datarepository) / sim_type / dd_type / f"{Tb:.1f}" / aggr_window / method
    )


def reproj(
    src_x: float, src_y: float, src_crs: str = "EPSG:4326", dst_crs: str = "EPSG:3035"
) -> Tuple[float, float]:
    """Reproject from one reference system to another.

    >>> # see: https://epsg.io/transform#s_srs=4326&t_srs=3035&x=11.0132789&y=45.5228261
    >>> # (lat, lon)
    >>> [f"{c:.2f}" for c in reproj(45.5228261, 11.0132789)]
    ["4400277.98", "2490583.97"]
    """
    trans = pyproj.Transformer.from_crs(src_crs, dst_crs)
    cy, cx = trans.transform(src_x, src_y)
    return (cx, cy)


@lru_cache()
def extract_by_dir(
    gdir: Path,
    lon: float,
    lat: float,
    refyear: int = None,
    refmonth: int = None,
    __datasets: Dict[str, rasterio.DatasetReader] = {},
):
    res = []
    idx = []
    # check inputs
    if refyear is not None and (refyear < 1950 or refyear > 2100):
        raise ValueError(
            f"Reference year must be 1950 <= refyear <=2100, instead is: {refyear}"
        )
    refyear = "*" if refyear is None else f"{refyear}"
    if refmonth is not None and (refmonth < 1 or refmonth > 12):
        raise ValueError(
            f"Reference month must be 1 <= refmonth <=12, instead is: {refmonth}"
        )
    refmonth = "*" if refmonth is None else f"{refmonth:02d}"

    # define the file pattern to match
    pattern = f"{refyear}_{refmonth}.tif"

    # Convert lat, lon to EPSG:3035 coords
    # cx, cy = reproj(lat, lon)
    cx, cy = reproj(src_x=lat, src_y=lon, src_crs="EPSG:4326", dst_crs="EPSG:3035")
    if not gdir.exists():
        res, idx = [], []
        yp, xp = -1, -1
    else:
        for gfi in gdir.iterdir():
            if gfi.match(pattern):
                idx.append(gfi.name[:-4].replace("_", "-"))
                try:
                    gx = __datasets[gfi.as_posix()]
                except KeyError:
                    gx = rasterio.open(gfi)
                    __datasets[gfi.as_posix()] = gx
                yp, xp = gx.index(cx, cy)
                if yp < 0 or xp < 0:
                    raise ValueError(
                        f"Negative row|col index, row_index={yp}, col_index={xp}"
                        f"@{lon:.{DECIMALS}f}({cx:.{DECIMALS}f}),{lat:.{DECIMALS}f}({cy:.{DECIMALS}f})"
                    )
                val = gx.read()[0][yp, xp]
                logging.info(
                    f"{gfi}@{lon:.{DECIMALS}f}({cx:.{DECIMALS}f}),{lat:.{DECIMALS}f}({cy:.{DECIMALS}f}):"
                    f" {yp}, {xp} => {val}"
                )
                res.append(val)
    sr = pd.Series(np.array(res), index=idx, name=f"yp={yp},xp={xp}")
    sr.sort_index(inplace=True)
    return sr
