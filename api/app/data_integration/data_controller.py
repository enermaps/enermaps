from app.data_integration import enermaps_server
from app.data_integration.data_config import get_ds_ids
from app.models.geofile import create


def init_enermaps_datasets():

    # Get NUTS and LAU datasets
    nuts_and_lau_datasets = ["country", "NUTS1", "NUTS2", "NUTS3", "LAU"]
    for dataset_name in nuts_and_lau_datasets:
        try:
            file_upload = enermaps_server.get_nuts_and_lau_dataset(dataset_name)
            if file_upload is not None:
                create(file_upload)
        except Exception as e:
            print("Error creating dataset {}".format(dataset_name))
            print(e)

    # [21, 24, 33, 35] : These datasets are tiled raster datasets (needing input coordinates)
    #                    and returning multiple images
    datasets_to_exclude = [
        1,
        2,
        3,
        4,
        5,
        6,
        9,
        11,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        24,
        27,
        28,
        29,
        39,
        31,
        33,
        35,
        42,
        43,
        45,
        46,
        47,
        48,
        49,
        50,
    ]
    datasets_to_exclude = []

    # Get the ids of the datasets that we want to load
    datasets_ids = get_ds_ids()

    # Check that the datasets that we want to load are in the enermaps DB
    for dataset_id in datasets_ids:
        if dataset_id not in datasets_to_exclude:
            try:
                file_upload = enermaps_server.get_dataset(dataset_id)
                if file_upload is not None:
                    create(file_upload)
            except Exception as e:
                print("Error creating dataset {}".format(dataset_id))
                print(e)
