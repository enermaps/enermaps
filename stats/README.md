# Stats

This service parses the database log to collect usage stats.

By running the service, a CSV file named `parsed_log.csv` will be produced containing for each query:

- timestamp
- dataset id
- IP address of the API user (to be confirmed)
- details of the query (parameters)


## Known issues

On Idiap server:
 - use `ubuntu:20.04`in `Dockerfile`
 - use `pandas==1.1.5` in `requirements.txt`
