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

# Parse log
queries = log.loc[
    log["message"].str.contains("enermaps_query"),
    ["log_time", "user_name", "connection_from", "message"],
]
queries["json_query"] = queries.message.str.extract(r"(?<=\(\')(.*)(?=\'\))")
queries["json_query"] = queries["json_query"].apply(lambda x: json.loads(x))
queries["ds_id"] = [d.get("data.ds_id") for d in queries.json_query]

# Export log of queries
queries.to_csv("stats/queries.csv")
