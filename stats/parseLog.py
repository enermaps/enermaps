#!/usr/bin/env python3
"""Parse Postgres log to retrieve the dataset ids and the IP of the API users."""

import argparse
import glob
import ipaddress
import json
import logging
import os
from urllib.parse import unquote

import pandas as pd
import sqlalchemy as sqla

# Limit to these postgrest queries
QUERY_STRINGS = ["enermaps_get_legend"]

# Limit to these caddy's URIS
URIs = [
    "/enermaps/api/datasets/legend/",
    "/enermaps/api/db/rpc/enermaps_get_legend?",
    "/enermaps/api/db/rpc/enermaps_query_geojson?",
    "/enermaps/api/db/rpc/enermaps_query_table?",
]

BASE_PATH_PG = "/stats/pg-logs/"
BASE_PATH_CADDY = "/stats/caddy-logs/"

SEL_COLS = ["timestamp", "ds_id", "country", "function", "json_query", "source"]

REMOVE = True  # remove old logs

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


def getCountry(log: pd.DataFrame):
    """Geolocate ip address."""

    def findCountry(ip, db, information="code"):
        try:
            ip = int(ipaddress.ip_address(ip))
            country = db.loc[(db["start"] < ip) & (db["end"] > ip), information].values[
                0
            ]
        except ValueError:
            country = "-"
        return country

    db = pd.read_csv("IP2LOCATION-LITE-DB1/IP2LOCATION-LITE-DB1.CSV", header=None)
    db.columns = ["start", "end", "code", "country"]
    log["country"] = ""
    log["country"] = log["ip"].apply(lambda x: findCountry(x, db))

    return log


def safelyJSONdecode(s: str):
    "Decode json-like string to dict, or keep it as a raw string."
    try:
        js = json.loads(s)
    except (json.decoder.JSONDecodeError, TypeError):
        js = {"raw_string": r"{}".format(s)}
    return js


def parseCADDYlog(log_file: str):
    """Parse the original caddy log file."""
    with open(log_file, "r") as f:
        dicts = f.read().splitlines()
    dicts = [json.loads(x) for x in dicts]
    log = pd.DataFrame.from_records(dicts)

    log["function"] = log["request"].apply(lambda x: x["uri"])
    log["ip"] = log["request"].apply(
        lambda x: x.get("headers").get("X-Forwarded-For")[0]
    )
    log["timestamp"] = pd.to_datetime(log["ts"], unit="s")
    log["ds_id"] = -1
    log["json_query"] = "{}"
    log.loc[log["function"].str.contains("raster"), "ds_id"] = (
        log.loc[log["function"].str.contains("raster"), "function"]
        .str.split("/")
        .str[-2]
    )
    log.loc[log["function"].str.contains("?parameters", regex=False), "json_query"] = (
        log.loc[log["function"].str.contains("?parameters", regex=False), "function"]
        .str.split("parameters=")
        .str[-1]
    )
    log["json_query"] = log["json_query"].apply(lambda x: unquote(x))
    log["json_query"] = log["json_query"].str.replace("+", "", regex=False)
    log["json_query"] = log["json_query"].apply(lambda x: safelyJSONdecode(x))

    log["time"] = pd.to_datetime(log["ts"], unit="s")

    selected = []
    for select in URIs:
        selected.append(log.loc[log["function"].str.startswith(select), :])

    parsed_log = pd.concat(selected)
    parsed_log["source"] = "caddy"
    return parsed_log


def parsePGlog(log_file: str):
    """Parse the original PG log file."""
    header = [
        "log_time",
        "user_name",
        "database_name",
        "process_id",
        "connection_from",
        "session_id",
        "session_line_num",
        "command_tag",
        "session_start_time",
        "virtual_transaction_id",
        "transaction_id",
        "error_severity",
        "sql_state_code",
        "message",
        "detail",
        "hint",
        "internal_query",
        "internal_query_pos",
        "context",
        "query",
        "query_pos",
        # "location" , # verbose off: no location available
        "application_name",
        "backend_type",
    ]
    try:
        log = pd.read_csv(log_file, header=None, on_bad_lines="skip", low_memory=False)
        log.columns = header
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        print("Cannot decode the content of the log file")
        log = pd.DataFrame()

    parsed_log = []

    if log.shape[0] > 0:
        print("Parsing")
        # Parse log
        # Standard SQL queries
        queries = log.loc[
            log["message"]
            .str.lower()
            .str.startswith("statement: select * from enermaps"),
            :,
        ]

        if queries.shape[0] > 0:
            queries["message"] = queries["message"].str.replace("\n", "")
            # Get the query
            queries["json_query"] = queries.message.str.extract(r"(?<=\(')(.*)(?='\))")
            queries["json_query"] = queries["json_query"].apply(
                lambda x: safelyJSONdecode(x)
            )
            # Get the dataset id
            ds_id = []
            for d in queries.json_query:
                parameters = d.get("parameters", {})
                if isinstance(parameters, str):
                    parameters = json.loads(parameters)
                if "data.ds_id" in parameters.keys():
                    ds_id.append(parameters.get("data.ds_id"))
                elif "id" in d.keys():
                    ds_id.append(parameters.get("id"))
                else:
                    ds_id.append(-1)
            queries["ds_id"] = ds_id
            parsed_log.append(queries)

        # Parse log
        # PostgREST queries
        queries = log.loc[
            (~log["detail"].isnull())
            & (
                log["message"].str.startswith("execute ")
            ),  # the parameters are saved in the detail field
            :,
        ]
        selected = []
        for string in QUERY_STRINGS:
            selected.append(queries.loc[queries.message.str.contains(string), :])
        queries = pd.concat(selected)
        if queries.shape[0] > 0:
            queries["detail"] = queries["detail"].str.replace("\n", "")
            # Get the query
            queries["json_query"] = queries["detail"].str.extract(
                r"(?<=\$1 = \')(.*)(?=')"
            )
            queries["json_query"] = queries["json_query"].apply(
                lambda x: safelyJSONdecode(x)
            )
            # Get the dataset_id
            ds_id = []
            for d in queries.json_query:
                if "id" in d.keys():
                    parameters = d
                else:
                    parameters = d.get("parameters", {})
                if isinstance(parameters, str):
                    parameters = json.loads(parameters)
                if "data.ds_id" in parameters.keys():
                    ds_id.append(parameters.get("data.ds_id"))
                elif "id" in parameters.keys():
                    ds_id.append(parameters.get("id"))
                else:
                    ds_id.append(-1)
            queries["ds_id"] = ds_id
            # Drop duplicate rows
            queries = queries.groupby("log_time").first().reset_index()

            # Find PostGrest function
            queries["function"] = queries["message"].str.extract(
                r'(?<=SELECT "public".")(.*)(?="\()'
            )

            # Find geolocalization info based on session_id
            geolocal = log.loc[log["session_id"].isin(queries["session_id"]), :]
            # Get the IP address
            geolocal = geolocal.loc[
                geolocal["message"].str.contains("request.header.x-forwarded-for"), :
            ]
            geolocal["ip"] = geolocal["message"].str.extract(
                r'(?<=request.header.x-forwarded-for" = \')(.*)(?=\';SET LOCAL'
                r' "request.header.x-forwarded-host" )'
            )

            # Merge geolocalization info with query info
            if geolocal.shape[0] > 0:
                queries = pd.merge(
                    geolocal[["ip", "session_id"]],
                    queries,
                    on="session_id",
                    how="outer",
                )
            else:
                queries["ip"] = None

            # Get only first ip
            queries["ip"] = queries["ip"].str.split(",").str[0]
            parsed_log.append(queries)

        # Concatenate the two types of query
        if len(parsed_log) > 0:
            parsed_log = pd.concat(parsed_log, ignore_index=True)
            parsed_log["log_time"] = pd.to_datetime(parsed_log["log_time"])
            parsed_log["timestamp"] = pd.to_datetime(parsed_log["session_start_time"])
            parsed_log = parsed_log.sort_values("session_start_time", ascending=True)

            # Drop duplicates
            parsed_log = (
                parsed_log.groupby(["session_start_time"], dropna=False)
                .first()
                .reset_index()
            )
            parsed_log["source"] = "pg"
            return parsed_log


def saveCSV(parsed_log: pd.DataFrame, parsed_log_file: str, sel_cols: list = SEL_COLS):
    print("Saving log file to {}".format(parsed_log_file))
    if not os.path.exists(parsed_log_file):
        parsed_log[sel_cols].iloc[0:0].to_csv(parsed_log_file, header=True, index=False)
    parsed_log[sel_cols].to_csv(parsed_log_file, mode="a", header=None, index=False)


if __name__ == "__main__":
    print("calling parsing")
    parser = argparse.ArgumentParser(description="Create log")
    parser.add_argument("--source_log_file", default="all", required=False)
    parser.add_argument("--parsed_log_file", "-o", default="tmp.csv", required=False)
    parser.add_argument("--sql", action="store_true")

    args = parser.parse_args()

    if args.source_log_file == "all":
        pglogs = []
        caddylogs = []
        # By default parse all the log files but the last one and remove them
        for log_file in sorted(
            glob.glob("{}*.csv".format(BASE_PATH_PG)), key=os.path.getmtime
        )[:-1]:
            print("Reading {}".format(log_file))
            pglog = parsePGlog(log_file)
            pglogs.append(pglog)
        if REMOVE:
            logging.info("Remove source pglog files")
            os.remove(log_file)
            log_file2 = log_file.replace(".csv", "")
            if os.path.exists(log_file2):
                os.remove(log_file2)

        for log_file in sorted(
            glob.glob("{}*.log".format(BASE_PATH_CADDY)), key=os.path.getmtime
        )[:-1]:
            print("Reading {}".format(log_file))
            caddylog = parseCADDYlog(log_file)
            caddylogs.append(caddylog)
            if REMOVE:
                logging.info("Remove source caddy log files")
                os.remove(log_file)
        logs = pd.concat([*pglogs, *caddylogs], ignore_index=True)
        pglogs = pd.concat(pglogs, ignore_index=True)
        caddylogs = pd.concat(caddylogs, ignore_index=True)
        # Geolocalize logs
        logs = getCountry(logs)
        # Prepare df
        logs = logs.loc[:, SEL_COLS]
        logs["json_query"] = logs["json_query"].apply(lambda x: json.dumps(x))
        if args.sql:
            db_engine = sqla.create_engine(DB_URL)
            logging.info("Loading to PostgreSQL...")
            logs.to_sql("stats", db_engine, if_exists="append", index=False)
            logging.info("Done.")
        else:
            saveCSV(pglog, os.path.abspath(os.path.join("stats", "pg_log.csv")))
    else:
        print("Manually loading log file")
        if "pg" in args.source_log_file:
            log = parsePGlog(
                os.path.abspath(os.path.join(BASE_PATH_PG, args.source_log_file))
            )
        elif "caddy" in args.source_log_file:
            log = parseCADDYlog(
                os.path.abspath(os.path.join(BASE_PATH_CADDY, args.source_log_file))
            )
        saveCSV(log, os.path.abspath(os.path.join(args.parsed_log_file)))
