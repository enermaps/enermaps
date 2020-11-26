base directory for the calculation modules (cm).

A calculation module is an asynchronous slow task (from seconds to hours of
latency for the answer). A calculation module takes a set of raster, a selection and an optional set of parameters

# Test a cm

Currently to test a particular cm, you will need to first start enermaps2 using docker-compose up in the root directory.
Then you can connect to the redis queue. The multiply cm is given as an example.

We strongly encourage you to write unittest that verify the good working of a calculation module separated from the enermaps2 api.

# Create a new cm

Each calculation module is a subdirectory in this directory.

It must contain:
* A setup.cfg symlink to the cm/setup.cfg file. (see
  https://mokacoding.com/blog/symliks-in-git/ for a brief explanation on symbolic links)
* A worker.py entrypoint, this must be an executable that start the worker.
* A test.py unittest testing the calculation without service dependencies.

# CMs interaction

Currently, the cm registers on the redis queue trough the celery library.
