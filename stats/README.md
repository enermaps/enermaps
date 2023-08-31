# Stats

This service parses the PostgreSQL and Caddy logs to collect usage stats.

The parsing will be contain the following information:

- timestamp
- ds_id: the EnerMaps datasetid (`-1` if not available)
- function: the PostGres function or the Caddy URI
- country: as localized from the IP address (if available) using IP2Location LITE data
- json_query: the query parameters, if available
- source: either `pg` or `caddy`


## Usage

To parse all the existing logs, run:

```bash
docker-compose -f docker-compose-db.yml run stats python3 parseLogs.py
```

A parsed CSV will be saved in the `/stats/parsed_logs` directory.

This command is meant to be run as a `cronjob` with these arguments:

```bash
docker-compose -f ../docker-compose-db.yml run stats python3 parseLogs.py --skip_last --sql --remove
```

Using `--skip_last`  the parsing will not be run on the last modified file, as this might still be written by PostGRES.

Using `--remove` source log files after parsing will be removed (except the last one, which might not be completed, if using `--skip_last`).

Using `--sql` the parsing will be appended into the `stats` table in the database, instead of the default CSV file.

## Manual parsing

It is also possible to parse a log file manually using the following command:

```bash
docker-compose -f docker-compose-db.yml run python3 parseLogs.py pglog_1600.csv
```

where `pglog_1600.csv` is the name of the log to be parsed.

An optional command `-o` can be set to change the name of the default output file `tmp.csv`.

Note that the `--remove`, `--skip_last` and `--sql` optios are not active for manual parsing.


## Acknowledgements
This module includes IP2Location LITE data available from http://www.ip2location.com.
