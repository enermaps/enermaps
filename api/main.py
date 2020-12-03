#!/usr/bin/env python
"""Entrypoint for the debug mode of flask,
For running this, you will need to have a local install
of all packages in requirements.txt. You can also
refer to the Dockerfile for the list of commands to run.

Due to a bug in flask package resulution, you will need to
run this script with the main.py as an absolute path, for example:

python $(pwd)/main.py

"""
from app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=7000, debug=True)
