#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 21:00:00 2021

Add list of datasets

@author: giuseppeperonato
"""
import json
import os
import logging
import pandas as pd
import sqlalchemy as sqla
import utilities

# Constants
logging.basicConfig(level=logging.INFO)

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

SCHEMA = "datasets_full"

if __name__ == "__main__":
    datasets = pd.read_csv("datasets.csv", engine="python", index_col=[0])
    datasets.drop(["di_script","di_URL"],inplace=True,axis=1) #remove di columns
    
    metadata = datasets.fillna("").to_dict(orient="records")
    metadata = [json.dumps(entry) for entry in metadata]
    
    data = pd.DataFrame()
    data["ds_id"] = datasets.index
    data["shared_id"] = datasets.shared_id.values
    data["metadata"] = metadata
    
    db_engine = sqla.create_engine(DB_URL)
    logging.info("Loading to PostgreSQL...")
    data.to_sql(SCHEMA, db_engine, if_exists="append", index=False)

