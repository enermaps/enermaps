import time

from flask import current_app

from app.data_integration import data_endpoints, enermaps_server
from app.models.geofile import create


def init_enermaps_datasets():
    """
    Downloads NUTS/LAU datasets and a default layer for each datasets
    whose parameters are stored in the configuration file.
    """
    # Get NUTS and LAU datasets
    nuts_and_lau_datasets = ["country", "NUTS1", "NUTS2", "NUTS3", "LAU"]
    for dataset_name in nuts_and_lau_datasets:
        try:
            time_started = time.time()
            current_app.logger.info(f"Get/update nuts/lau <{dataset_name}>...")
            file_upload = enermaps_server.get_nuts_and_lau_dataset(dataset_name)
            time_fetched = time.time()
            current_app.logger.info(
                f"... fetch done in {int(time_fetched - time_started)} seconds"
            )
            if file_upload is not None:
                create(file_upload)
                time_saved = time.time()
                current_app.logger.info(
                    f"... save done in {int(time_saved - time_fetched)} seconds."
                )
        except Exception as e:
            current_app.logger.error("Error creating dataset {}".format(dataset_name))
            current_app.logger.error(e)

    # Get the ids of the datasets that we want to load from the configuration file
    datasets_ids = data_endpoints.get_ds_ids()
    # To download only a subset of the datasets (!datasets ids must be in the config file!)
    # datasets_ids = [1,2,3,4,5,6]
    for dataset_id in datasets_ids:
        try:
            time_started = time.time()
            current_app.logger.info(f"Get/update dataset <{dataset_id}>...")
            file_upload = enermaps_server.get_dataset(dataset_id)
            time_fetched = time.time()
            current_app.logger.info(
                f"... fetch done in {int(time_fetched - time_started)} seconds"
            )
            if file_upload is not None:
                create(file_upload)
                time_saved = time.time()
                current_app.logger.info(
                    f"... save done in {int(time_saved - time_fetched)} seconds."
                )
        except Exception as e:
            current_app.logger.error("Error creating dataset {}".format(dataset_id))
            current_app.logger.error(e)
