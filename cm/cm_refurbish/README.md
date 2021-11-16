# CM REFURBISH SCENARIOS BUILDER

## Objective

The objective of this CM is to Assess the impact of different building refurbishment scenarios​.

## How it works

### Prerequisite

EnerMaps have to be launched.
If this is not yet the case, see [the general README](../../README.md) to find out how to do so.

Once EnerMaps launched, the frontend should be available on this adress : http://127.0.0.1:7000.

## Inputs

### Data used by the CM

* HDD from EnerMaps CM​
* CDD from Enermaps CM
* Building stock dataset from HotMaps (at national level)​
* EU population or EU buildings footprint (as spatial proxy to scale down from NUTS0 to LAU2)


### User inputs

* Select the target year (e.g., 2050)​
* Select the refurbish rate per sector, epoch of construction and building typology​
* Select the location (from LAU2 up to EU27)

## Ouputs

As an output, we get the following data :
* the whole heating energy demand
* the whole cooling energy demand
* the yearly heating demand
* the monthly heating demand
* the yearly cooling demand
* the monthly cooling demand
