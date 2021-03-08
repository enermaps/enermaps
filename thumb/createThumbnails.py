#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This sample script creates sample thumbnails for each dataset.
They will be replaced by the actual thumbnails later on.

@author: giuseppeperonato
"""

import pandas as pd
import shutil
import os
datasets = pd.read_csv("datasets.csv",index_col=0)
datasets = datasets.dropna()

for i, ds in datasets.iterrows():
	pid = ds.PID.replace("http://","")
	pid = pid.replace("https://","")
	dest_fpath = os.path.join("img",pid)
	os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)
	shutil.copy("dummy.png",os.path.join("img",pid)+".png")