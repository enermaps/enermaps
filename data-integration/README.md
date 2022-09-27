# Data integration for EnerMaps

This service retrieves the different sources to be integrated into the database.

## Available pipelines

At the moment the service does not run any command.
You can manually execute the available pipelines with the following commands:

  - 0: Admin units (LAU NUTS)
    `docker-compose -f ../docker-compose-db.yml run data-integration admin_units.py`

Remember to start the db service via `docker-compose --file ../docker-compose-db.yml up -d db` before running the pipelines.

## Required files

