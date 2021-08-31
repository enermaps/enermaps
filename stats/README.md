# Stats

This service parses the database log to collect usage stats.

A CSV file named `parsed_log.csv` will be produced containing for each query.

- timestamp
- dataset id
- IP address of the API user
- details of the query (parameters)

Note that the parsing will not be run on the last modified file, as this might still be written by PostGRES.

Source log files after parsing will be removed (except the latest one, which might not be completed).

## Usage

To parse all the existing logs, run:

```bash
docker-compose -f docker-compose-db.yml run stats python3 parseLog.py all
```

This command is meant to be run by `cron` like hourly routine.

## Manual parsing

It is also possible to parse a log file manually (the source file in this case will not be removed) using the following command:

```bash
docker-compose -f docker-compose-db.yml run python3 parseLog.py pglog_1600.csv
```

where `pglog_1600.csv` is the name of the log to be parsed.

The log files produced by the db can be listed with this command:

```bash
docker-compose -f docker-compose-db.yml run stats ls -lh /db-data/pg_log
```

An optional command `-o`can be set to change the name of the default output file `tmp.csv`.


## Known issues

On Idiap server:
 - use `ubuntu:20.04`in `Dockerfile`
 - use `pandas==1.1.5` in `requirements.txt`
