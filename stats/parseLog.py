#!/usr/bin/env python3
"""Parse Postgres log to retrieve the dataset ids and the IP of the API users."""

import argparse
import glob
import json
import os

import pandas as pd

# Limit to these postgrest queries
QUERY_STRINGS = [""]


def parseLog(log_file: str, parsed_log_file: str):
    """Parse the original log file."""
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
        log = pd.read_csv(
            log_file, header=None, error_bad_lines=False, low_memory=False
        )
        log.columns = header
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        print("Cannot decode the content of the log file")
        log = pd.DataFrame()

    parsed_log = []

    def safelyJSONdecode(s: str):
        "Decode json-like string to dict, or keep it as a raw string."
        try:
            js = json.loads(s)
        except (json.decoder.JSONDecodeError, TypeError):
            js = {"raw_string": r"{}".format(s)}
        return js

    if log.shape[0] > 0:
        print("Parsing")
        # Parse log
        # Standard SQL queries
        queries = log.loc[
            log["message"]
            .str.lower()
            .str.startswith("statement: select * from enermaps"),
            ["log_time", "message"],
        ]
        if queries.shape[0] > 0:
            queries["message"] = log["message"].str.replace("\n", "")
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
            ~log["detail"].isnull(),  # the parameters are saved in the detail field
            ["log_time", "message", "detail", "session_id", "session_line_num"],
        ]
        for string in QUERY_STRINGS:
            queries = queries.loc[queries.message.str.contains(string), :]
        if queries.shape[0] > 0:
            print("PostgREST queries")
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
            queries = queries.groupby("session_id").first()

            # Find PostGrest function
            queries["function"] = queries["message"].str.extract(
                r'(?<=SELECT "public".")(.*)(?="\()'
            )
            # Find geolocalization info based on session_id
            geolocal = log.loc[log["session_id"].isin(queries.index), :]
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
                    geolocal[["ip", "session_id"]], queries, on="session_id"
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
            parsed_log = parsed_log.sort_values("log_time", ascending=True)

            # Drop duplicates
            parsed_log = (
                parsed_log.groupby(["log_time", "ip", "function"], dropna=False)
                .first()
                .reset_index()
            )

            # Append to file parsed log of queries
            print("Saving log file to {}".format(parsed_log_file))
            sel_cols = ["log_time", "ds_id", "ip", "function", "json_query"]
            if not os.path.exists(parsed_log_file):
                parsed_log[sel_cols].iloc[0:0].to_csv(
                    parsed_log_file, header=True, index=False
                )
            parsed_log[sel_cols].to_csv(
                parsed_log_file, mode="a", header=None, index=False
            )


if __name__ == "__main__":
    print("calling parsing")
    parser = argparse.ArgumentParser(description="Create log")
    parser.add_argument("source_log_file", default="all")
    parser.add_argument("--parsed_log_file", "-o", default="tmp.csv", required=False)

    args = parser.parse_args()

    if args.source_log_file == "all":
        # By default parse all the log files but the last one and remove them
        for log_file in sorted(
            glob.glob("/db-data/pg_log/*.csv"), key=os.path.getmtime
        )[:-1]:
            print("Reading {}".format(log_file))
            parseLog(log_file, os.path.abspath(os.path.join("stats", "parsed_log.csv")))
            # Remove source log files
            os.remove(log_file)
            log_file2 = log_file.replace(".csv", "")
            if os.path.exists(log_file2):
                os.remove(log_file2)
    else:
        print("Manually loading log file")
        parseLog(
            os.path.abspath(os.path.join("db-data", "pg_log", args.source_log_file)),
            os.path.abspath(os.path.join("stats", args.parsed_log_file)),
        )
