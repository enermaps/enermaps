#!/usr/bin/env python3
"""
Add list of datasets.
This is temporary to feed a table which is used for the OpenAire APIs.

The following table must exist:
```sql
CREATE TABLE public.datasets_full
(
    ds_id int PRIMARY KEY,
    shared_id char(300),
    metadata jsonb
);
```

@author: giuseppeperonato
"""
import json
import logging
import os

import pandas as pd
import sqlalchemy as sqla

# Constants
logging.basicConfig(level=logging.INFO)

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
EXCLUDED_FROM_JSON = ["shared_id", "isInEDMT"]


if __name__ == "__main__":
    datasets = pd.read_csv("datasets_full.csv", engine="python", index_col=[0])
    datasets.drop(["di_script", "di_URL"], inplace=True, axis=1)  # remove di columns

    # Format the date
    datasets["Publication Date"] = pd.to_datetime(datasets["Publication Date"]).astype(
        str
    )

    # Remove end of line chars
    datasets = datasets.replace("\\n", "", regex=True)

    metadata = (
        datasets.loc[
            :,
            [column for column in datasets.columns if column not in EXCLUDED_FROM_JSON],
        ]
        .fillna("")
        .to_dict(orient="records")
    )
    metadata = [json.dumps(entry) for entry in metadata]

    data = pd.DataFrame()
    data["ds_id"] = datasets.index
    data["shared_id"] = datasets.shared_id.values
    data["metadata"] = metadata

    db_engine = sqla.create_engine(DB_URL)
    logging.info("Loading to PostgreSQL...")
    data.to_sql(SCHEMA, db_engine, if_exists="append", index=False)
