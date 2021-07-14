# Stats

This service parses the database log to collect usage stats.

By running the service, a cron job will be initiated parsing the original log files every hour (at minute 5).
A CSV file named `parsed_log.csv` will be produced containing for each query.

- timestamp
- dataset id
- IP address of the API user
- details of the query (parameters)

Note that the parsing will not be run on the last modified file, as this might still be written by PostGRES.

Source log files after parsing will be removed.

## Manual parsing

It is also possible to parse a log file manually (the source file in this case will not be removed) using the following command:

```bash
docker-compose exec stats python3 parseLog.py pglog_1600.csv
```

where `pglog_1600.csv` is the name of the log to be parsed.

The log files produced by the db can be listed with this command:
```bash
docker-compose exec db ls -lh var/lib/postgresql/data/pg_log
```

An optional command `-o`can be set to change the name of the default output file `tmp.csv`.


## Known issues

On Idiap server:
 - use `ubuntu:20.04`in `Dockerfile`
 - use `pandas==1.1.5` in `requirements.txt`
