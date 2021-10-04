# Utility to schedule jobs

These utilities are used to run periodical routines on the host machine.
We use Unix `cron` on the host machine, hence not directly in Docker, to run the Docker containers.

Here are the jobs currently implemented:

- `data-integration.sh`contains the data-integration pipelines that have to be run twice per year. Biannual jobs are run *at 02:00 on day-of-month 1 in March and September*.

- `db-stats.sh` runs hourly (*at minute 5*) the `stats` services to parse the db logs.


## Usage

- Copy the `config` file to the `/etc/enermaps` directory:

```bash
$ sudo mkdir /etc/enermaps
$ sudo cp config /etc/enermaps/
```

- Edit the `/etc/enermaps/config` file to set the ENERMAPS_ROOT variable to the path to the EnerMaps root directory
- Copy the `crontab.txt` file to `/etc/cron.d/`:

```bash
$ sudo cp crontab.txt /etc/cron.d/enermaps
$ sudo chown root:root /etc/cron.d/enermaps
```
