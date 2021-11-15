#!/bin/bash

# Load variables
export $(grep -v '^#' /etc/enermaps/config | xargs)

# Run pipelines
echo 'getPVGIS DS 1'
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getPVGIS.py
echo

echo 'getJRC_GEOPP_DB DS 2'
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getJRC_GEOPP_DB.py
echo

echo 'getJRC-hydro-power DS 3'
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getJRC-hydro-power.py
echo

echo 'getJRC-PPDB-OPEN DS 4'
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getJRC-PPDB-OPEN.py
echo

echo 'getEEA DS 5'
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getEEA.py
echo

echo 'getEurostat DS 6, 9, 22, 42, 47, 48, 49, 50'
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getEurostat.py

echo 'getElectricity DS 7'
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getElectricity.py
echo

echo 'getPopulation DS 8'
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getPopulation.py
echo

echo 'getSETIS DS 11'
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getSETIS.py
echo

echo 'getPANGAEA DS 14'
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getPANGAEA.py
echo

echo 'getEra5 DS 15, 20'
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getEra5.py
echo

# 16, 17 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getEMHIRES.py

echo 'getEnergydata DS 18'
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getEnergydata.py
echo

echo 'getEdgar DS 19'
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getEdgar.py

# 21 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getESM-EUDEM.py

# 23 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getWater.py

# 24 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getSolarAtlas.py

echo 'getHotMaps_raster DS 25, 31, 43, 45'
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getHotMaps_raster.py
echo

# 27 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getS2BIOM.py

echo 'getHotMaps_tabular DS 28'
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getHotMaps_tabular.py
echo

# 29 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getSET-Nav.py

# 30 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getENER.py

# 33 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getBuildingHeight.py

# 35 will not be updated
# echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getESM-EUDEM.py

echo 'getOECD DS 46'
echo $(date -u) && docker-compose -f $ENERMAPS_ROOT/docker-compose-production.yml run --rm data-integration getOECD.py
