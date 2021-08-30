#!/bin/bash
# Load variables
export $(grep -v '^#' ~/.enermaps | xargs)

# Run pipelines
# 1
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getPVGIS.py
# 2
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getJRC_GEOPP_DB_csv.py
# 3
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getJRC_hydro-power.py
# 4
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getJRC_PPDB-OPEN.py
# 5
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getEEA.py
# 6, 9, 22, 42, 47, 48, 49, 50
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getEurostat.py
# 7
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getElectricity.py
# 8
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getPopulation.py
# 11
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getSETIS.py
# 14
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getPANGAEA.py
# 15, 20
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getEra5.py
# 16, 17 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getEMHIRES.py
# 18
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getEnergydata.py
# 19
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getEdgar.py
# 21 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getESM-EUDEM.py
# 23 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getWater.py
# 24 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getSolarAtlas.py
# 25, 31, 43, 45
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getHotMaps_raster.py
# 27 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getS2BIOM.py
# 28
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getHotMaps_tabular.py
# 29 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getSET-Nav.py
# 30 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getENER.py
# 33 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getBuildingHeight.py
# 35 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getESM-EUDEM.py
# 46
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-db.yml run data-integration getOECD.py
