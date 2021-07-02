# HeatLearn

The *HeatLearn* CM is an implementation of a CNN model to predict aggregated building heating energy demand from ESM land-use maps.

## How it works

### Prerequisite

EnerMaps has to be launched.
If this is not yet the case, see [the general README](../../README.md) to find out how to do so.

Once EnerMaps launched, the frontend should be available on this adress : http://127.0.0.1:7000.

The API key of the PostgREST API must be placed in a text file `cm/heatlearn/API_KEY.txt`.

### Inputs

To make the CM work, we need three inputs:

* the raster we want to study (TBD: should be forced to ESM);
* the boundary of the area we want to study;
* the tile size;
* the year (to obtain Heating Degree Days from Eurostat);

Heating Degree Days (HDD) are obtained at the NUTS3 level from dataset 9 (Eurostat), including EU countries only.
Pre-computed HDD for the Canton of Geneva are also available.

### Ouputs

As an output, we get the following data:
* a false-color raster representing the absolute heating demand for each tile;
* aggregated results for all tiles within the boundary;
