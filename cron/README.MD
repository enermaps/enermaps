# Utility to schedule jobs

These utilities are used to run periodical routines on the host machine.
We use Unix `cron` on the host machine, hence not directly in Docker, to run the Docker containers.

Here are the jobs currently implemented:

- `data-integration.sh`contains the data-integration pipelines that have to be run twice per year. Biannual jobs are run *at 02:00 on day-of-month 1 in March and September*.


## Usage

- Copy the `.enermaps` to your HOME directory `cp .enermaps ~/.enermaps`.

- Edit the `~/.enermaps` file to set the ENERMAPS_ROOT variable to the path to the EnerMaps root directory

- Append to your user crontab the content of the `crontab.txt` file.
Use for example `EDITOR=nano crontab -e` to open your user crontab in `nano`.
