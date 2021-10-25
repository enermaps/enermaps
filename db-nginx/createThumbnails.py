#!/usr/bin/env python3
"""
This script creates sample thumbnails for each dataset.
It expects screenshots to be placed in the screenshots directory,
otherwise dummy images are used.
Source screenshots should be named {shared_id}.png.

@author: giuseppeperonato
"""

import os
import shutil

import pandas as pd
from PIL import Image

# Target size of thumbnails
THUMBSIZE = (640, 360)

# Parameters for processing screenshots
# Change here depending on your source files
SCREENSHOT_SIZE = (3582, 1960)
RESIZED = (658, 360)
CROP_AREA = (0, 0, 640, 360)  # left, upper, right, lower

datasets = pd.read_csv("../data-integration/datasets.csv", index_col=0)

for i, ds in datasets.iterrows():
    pid = ds["shared_id"]
    dest = os.path.join("web", "images", pid + ".png")
    source = os.path.join("screenshots", pid + ".png")
    if os.path.exists(source):
        img = Image.open(source)
        if img.size == SCREENSHOT_SIZE:
            img = img.resize(RESIZED, Image.ANTIALIAS)
            img = img.crop(CROP_AREA)
            if img.size == THUMBSIZE:
                img.save(dest)
                print(pid, "imported screenshot")
            else:
                print(pid, "the screenshot output size is not correct.")
        else:
            print(pid, "the screenshot input size is not correct.")
    else:
        if not os.path.exists(dest):
            shutil.copy("dummy.png", dest)
