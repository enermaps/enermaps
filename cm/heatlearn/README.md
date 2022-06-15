# CM - AI-estimated Building Heat Demand ("HeatLearn")


## Objective
The *HeatLearn* CM is an implementation of a CNN model to predict aggregated building heating energy demand from ESM land-use maps.

## How it works

This calculation module uses a land-use map (ESM) and Heat Degree Days (HDD) dataset to deploy a data-driven method for determining aggregated annual heating demand. In the toolbox, the user can only use the following dataset included in the EnerMaps database:

- the [European Settlement Map 2012 - release 2017 (ESM)](https://land.copernicus.eu/pan-european/GHSL/european-settlement-map/esm-2012-release-2017-urban-green) land use map

In the backend, the CM will also query the following dataset using the EnerMaps API:

- [JRC](https://ec.europa.eu/eurostat/cache/metadata/en/nrg_chdd_esms.htm) Heating Degree Days (HDD) available through Eurostat.

There is no need to select this layer in the frontend.

The model has been trained on a dataset of building heating consumption from the Canton of Geneva (IDC). This means that it was trained to find how the features expressed by the ESM land use map influence the building annual heating demand.


## Prerequisite

EnerMaps has to be launched.
If this is not yet the case, see [the general README](../../README.md) to find out how to do so.

Once EnerMaps launched, the frontend should be available on this adress : http://127.0.0.1:7000.

The API key of the PostgREST API must be placed in a text file `cm/heatlearn/API_KEY.txt`.

## Inputs

- Parameters:
  - _Year_ [-], acceptable values: [1980-2020]. The upper boundary might be updated according to EnerMaps data update policy.
  - _Tile size_ [m], acceptable values: [500, 300 m], corresponding to 0.25 and 0.3 km<sup>2</sup>
  - The polygon(s) of a region. This might be the selection of one or multiple administrative units (e.g. LAU/NUTS), or a polygon drawn by the user in the interface. This is limited to a maximum area of 200 km<sup>2</sup> to provent too large requests.
- Layers:
  - European Settlement Map
    _ in raster format (\*.tif)
    _ with 2.5 m resolution
  - JRC Heating Degree Days \* in EnerMaps format (currently obtained through the PostgREST API).

## Ouputs

- Parameters:

  - _Annual heating demand_ in the selected region [_**GWh**_]
  - _Heating density_ in the selected region [_**MWh/ha**_]
  - _Heating Degree Days_ in the selected region [_**°C**_]

- Layers:
  - False color map format of the _Annual heating demand_. The color classes are automatically generated based on Jenks natural breaks classification method.
    - in raster format (\*.tif)
    - EPSG:3035 projection
    - the resolution depends on the _Tile size_ input parameter.


## Wiki

Further information on the calculation module methodology can be found [here](https://enermaps-wiki.herokuapp.com/en/HeatLearn.md).