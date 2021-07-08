#!/usr/bin/env python3
"""Parse Postgres log sto retrieve the dataset ids and the IP of the API users."""

import json

import pandas as pd

# Load log
log = "/db-data/pg_log/postgresql.csv"
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
log = pd.read_csv(log, header=None)
log.columns = header

parsed_log = []

# Parse log
# Standard SQL queries
queries = log.loc[
    log["message"].str.lower().str.startswith("statement: select * from enermaps"),
    ["log_time", "message"],
]
queries["message"] = log["message"].str.replace("\n", "")
# Get the query
queries["json_query"] = queries.message.str.extract(r"(?<=\(')(.*)(?='\))")
queries["json_query"] = queries["json_query"].apply(lambda x: json.loads(x))
# Get the dataset id
queries["ds_id"] = [d.get("data.ds_id") for d in queries.json_query]

parsed_log.append(queries)

# Parse log
# PostgREST queries
queries = log.loc[
    ~log["detail"].isnull(),  # the parameters are saved in the detail field
    ["log_time", "message", "detail", "session_id", "session_line_num"],
]
queries["detail"] = queries["detail"].str.replace("\n", "")
# Get the query
queries["json_query"] = queries["detail"].str.extract(r"(?<=parameters\": )(.*)(?=\}')")
queries["json_query"] = queries["json_query"].apply(lambda x: json.loads(x))
# Get the dataset_id
queries["ds_id"] = [d.get("data.ds_id") for d in queries.json_query]

# Drop duplicate rows
queries = queries.groupby("session_id").first()

# Find geolocalization info based on session_id
geolocal = log.loc[log["session_id"].isin(queries.index), :]
# Get the IP address
geolocal = geolocal.loc[
    geolocal["message"].str.contains("request.header.x-forwarded-for"), :
]
geolocal["ip"] = geolocal["message"].str.extract(
    r'(?<=request.header.x-forwarded-for" = \')(.*)(?=\';SET LOCAL "request.header.x-forwarded-host" )'
)

# Merge geolocalization info with query info
queries = pd.merge(geolocal[["ip", "session_id"]], queries, on="session_id")

parsed_log.append(queries)


# Concatenate the two types of queries
parsed_log = pd.concat(parsed_log, ignore_index=True)
parsed_log = parsed_log.sort_values("log_time")

# Export parsed log of queries
parsed_log[["log_time", "ds_id", "ip", "json_query"]].to_csv("stats/parsed_log.csv")
