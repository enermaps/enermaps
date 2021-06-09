"""This module manages the interaction of the api with a postgresdb
"""
import logging

from flask import g, current_app
import psycopg2


def teardown_db(_):
    """Cleanup the db when the app the exiting the context.
    see https://flask.palletsprojects.com/en/1.1.x/tutorial/database/
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def get_db():
    """Create the database connection when it is needed
    """
    if "db" not in g:
        try:
            g.db = psycopg2.connect(
                host=current_app.config["DB_HOST"],
                password=current_app.config["DB_PASSWORD"],
                database=current_app.config["DB_DB"],
                user=current_app.config["DB_USER"],
            )
        except psycopg2.OperationalError as err:
            if not current_app.config["TESTING"]:
                logging.error("Cannot connect to postgres: %s", err)

            g.db = None

    return g.db
