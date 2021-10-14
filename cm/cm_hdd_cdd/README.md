# HDD & CDD SCENARIOS BUILDER

## Objective

The objective of this CM is to assess the heating and cooling demand in Europe up to 2050, 2100.
The CM returns the monthly and yearls Heating Degree Days (HDD) and Cooling Degree Days (CDD) for a user selected scenario from the [EURO CORDEX](https://euro-cordex.net/) repositories.


## How it works

### Prerequisite

EnerMaps have to be launched.
If this is not yet the case, see [the general README](../../README.md) to find out how to do so.

Once EnerMaps launched, the frontend should be available on this adress : http://127.0.0.1:7000.

## Inputs

### Data used by the CM

Observations:​

* Daily temperature obs. from regional/national monitoring station networks ​
* Daily temperature [E-OBS](https://www.ecad.eu/dailydata/index.php) dataset (European coverage) at ~25 km​


Climate simulations (EURO CORDEX):​

* Daily temperature EURO CORDEX historical simulations at ~12.5 km​
* Daily temperature EURO CORDEX scenario simulations for RCP 4.5 and 8.5 at ~12.5 km


### User inputs

Mandatory:​

* Select a point from the map​
* Select the reference year (present baseline, 2050, 2100)​
* Select the scenario RCP (4.5 or 8.5)​

Optional:​

* Select the base temperature for HDD (default: 18°C)​
* Select the base temperature for CDD (default: 22°C)


## Run the CM

To start the CM, simply press the launch button.


## Ouputs

As an output, we get the following data :
* the start of the task ID
* the status of the task
* the annual HDD and CDD
* the monthly HDD and CDD
