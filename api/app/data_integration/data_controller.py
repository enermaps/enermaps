from app.data_integration import enermaps_server
from app.models.geofile import create


def init_enermaps_datasets():

    # Get NUTS and LAU datasets
    # nuts_and_lau_datasets = ["country", "NUTS1", "NUTS2", "NUTS3", "LAU"]
    # for dataset_name in nuts_and_lau_datasets:
    #     try:
    #         file_upload = enermaps_server.get_nuts_and_lau_dataset(dataset_name)
    #         if file_upload is not None:
    #             create(file_upload)
    #     except Exception as e:
    #         print("Error creating dataset {}".format(dataset_name))
    #         print(e)

    # These datasets are tiled raster datasets (needing input coordinates)
    # and returning multiple images
    # datasets_to_exclude = [21, 24, 33, 35]
    datasets_to_exclude = []

    # Get the ids of the datasets that we want to load
    datasets_ids = enermaps_server.get_datasets_ids()

    # Get all the metadata off all the datasets that are in the enermaps DB
    metadata = enermaps_server.get_datasets_metadata()

    # Check that the datasets that we want to load are in the enermaps DB,
    # and get the human readable name of the dataset
    datasets_to_retrieve = []
    for dataset_id in datasets_ids:
        if dataset_id not in datasets_to_exclude:
            for value in metadata:
                try:
                    if value["ds_id"] == dataset_id:
                        dataset_name = value["title"]
                        datasets_to_retrieve.append((dataset_id, dataset_name))
                except KeyError:
                    print(
                        "Dataset key error skipping dataset {}".format(str(dataset_id))
                    )

    for dataset_id, dataset_name in datasets_to_retrieve:
        try:
            file_upload = enermaps_server.get_dataset(dataset_id, dataset_name)
            if file_upload is not None:
                create(file_upload)
        except Exception as e:
            print("Error creating dataset {}".format(dataset_id))
            print(e)
