#!/usr/bin/env python3
"""
Add metadata for datasets which will not be displayed in the EDMT.

@author: giuseppeperonato
"""
import json
import logging

import pandas as pd
import utilities

# Constants
logging.basicConfig(level=logging.INFO)

DB_URL = utilities.DB_URL


if __name__ == "__main__":
    datasets = pd.read_csv("datasets.csv", index_col=[0])
    ds_ids = list(datasets.loc[~datasets["isInEDMT"], :].index)

    for ds_id in ds_ids:
        logging.info("Retrieving metadata for dataset {}".format(ds_id))

        if utilities.datasetExists(
            ds_id,
            DB_URL,
        ):
            utilities.removeDataset(ds_id, DB_URL)
            logging.info("Removed existing dataset")

        # Create dataset table
        metadata = datasets.loc[ds_id].fillna("").to_dict()
        metadata = json.dumps(metadata)
        dataset = pd.DataFrame(
            [
                {
                    "ds_id": ds_id,
                    "metadata": metadata,
                    "shared_id": datasets.loc[ds_id, "shared_id"],
                }
            ]
        )
        utilities.toPostgreSQL(
            dataset,
            DB_URL,
            schema="datasets",
        )
