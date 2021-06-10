#!/usr/bin/env python
"""Entrypoint for the debug mode of flask,
For running this, you will need to have a local install
of all packages in requirements.txt. You can also
refer to the Dockerfile for the list of commands to run.

Due to a bug in flask package resulution, you will need to
run this script with the main.py as an absolute path, for example:

python $(pwd)/main.py

"""
import os
import signal
from app import create_app
import bjoern


NUM_WORKERS = 4
worker_pids = []
app = create_app()
bjoern.listen(app, "0.0.0.0", 80)

for _ in range(NUM_WORKERS):
    pid = os.fork()
    if pid > 0:
        worker_pids.append(pid)
    elif pid == 0:
        try:
            bjoern.run()
        except KeyboardInterrupt:
            pass
        exit()

try:
    for _ in range(NUM_WORKERS):
        os.wait()
except KeyboardInterrupt:
    for pid in worker_pids:
        os.kill(pid, signal.SIGINT)
