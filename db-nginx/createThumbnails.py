#!/usr/bin/env python3
"""
This sample script creates sample thumbnails for each dataset.
They will be replaced by the actual thumbnails later on.

@author: giuseppeperonato
"""

import os
import shutil

import pandas as pd

datasets = pd.read_csv("../data-integration/datasets_full.csv", index_col=0)

for i, ds in datasets.iterrows():
    pid = ds["shared_id"]
    dest_fpath = os.path.join("web", "images", pid)
    os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)
    shutil.copy("dummy.png", os.path.join("web", "images", pid) + ".png")
