#!/bin/bash

# Load variables
export $(grep -v '^#' /etc/enermaps/config | xargs)

# Run pipelines
# 1
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getPVGIS.py
# 2
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getJRC_GEOPP_DB_csv.py
# 3
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getJRC_hydro-power.py
# 4
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getJRC_PPDB-OPEN.py
# 5
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getEEA.py
# 6, 9, 22, 42, 47, 48, 49, 50
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getEurostat.py
# 7
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getElectricity.py
# 8
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getPopulation.py
# 11
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getSETIS.py
# 14
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getPANGAEA.py
# 15, 20
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getEra5.py
# 16, 17 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getEMHIRES.py
# 18
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getEnergydata.py
# 19
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getEdgar.py
# 21 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getESM-EUDEM.py
# 23 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getWater.py
# 24 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getSolarAtlas.py
# 25, 31, 43, 45
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getHotMaps_raster.py
# 27 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getS2BIOM.py
# 28
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getHotMaps_tabular.py
# 29 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getSET-Nav.py
# 30 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getENER.py
# 33 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getBuildingHeight.py
# 35 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getESM-EUDEM.py
# 46
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run --rm data-integration getOECD.py
