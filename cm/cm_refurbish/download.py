#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path

import urllib3

# define main paths
CMDIR = Path(__file__).parent
DATADIR = CMDIR / "data"

if not DATADIR.exists():
    # create data dir if not exists
    os.makedirs(DATADIR, exist_ok=True)

# Building stock data from hotmaps
csv_path = DATADIR / "building_stock.csv"
if not csv_path.exists():
    csv_url = (
        "https://gitlab.com/hotmaps/building-stock/-/raw/master/data/building_stock.csv"
    )
    http = urllib3.PoolManager()
    print(f"Downloading building stock data\n  - from: {csv_url}\n  - to: {csv_path}")
    with http.request("GET", csv_url, preload_content=False) as csv_req, open(
        csv_path, "b+w"
    ) as csv_file:
        csv_file.write(csv_req.read())
    print("Done!")
else:
    print(f"Building stock file already exists: {csv_path}. Download SKIPPED!")


pop_path = DATADIR / "LAU_RG_01M_2020_3035.geojson"
if not pop_path.exists():
    pop_url = "https://gisco-services.ec.europa.eu/distribution/v2/lau/geojson/LAU_RG_01M_2020_3035.geojson"
    http = urllib3.PoolManager()
    print(f"Downloading population data\n  - from: {pop_url}\n  - to: {csv_path}")
    with http.request("GET", pop_url, preload_content=False) as pop_req, open(
        pop_path, "b+w"
    ) as pop_file:
        pop_file.write(pop_req.read())
    print("Done!")
else:
    print(f"Population file already exists: {pop_path}. Download SKIPPED!")
