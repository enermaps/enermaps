# CM - Scenarios of Heating and Cooling Degree Days

The objective of this CM is to assess the heating and cooling demand in Europe up to 2050, 2100.
The CM returns the monthly and yearls Heating Degree Days (HDD) and Cooling Degree Days (CDD) for a user selected scenario from the [EURO CORDEX](https://euro-cordex.net/) repositories.


## How it works
This calculation module uses the EURO-CORDEX simulation ensemble at 0.11 degrees of spatial resolution from historical and future scenarios, under different assumptions of [Representative Concentration Pathway (RCP)](https://en.wikipedia.org/wiki/Representative_Concentration_Pathway) of 2.6, 4.5 and 8.5. In the toolbox, the user can select:

- the reference year;
- the RCP scenarios;
- the base temperature to compute the HDD and the CDD.

Note that the CM is considering 297 simulations using different regional and local models and boundary conditions. The values returned to the user are the statical values extracted from the whole set of simulations.

### Prerequisite

EnerMaps have to be launched.
If this is not yet the case, see [the general README](../../README.md) to find out how to do so.

Once EnerMaps launched, the frontend should be available on this adress : http://127.0.0.1:7000.

## Inputs

- Parameters:
  - _Reference year_ [-], acceptable values: [1950-2100];
  - _Representative Concentration Pathway (RCP)_, acceptable values [RCP](https://en.wikipedia.org/wiki/Representative_Concentration_Pathway): [2.6, 4.5, 8.5];
  - _Base temperatire for Heating Degreee Days_, acceptable values: [10-25 °C];
  - _Base temperatire for Cooling Degreee Days_, acceptable values: [15-30 °C];
- Layers:
  - HDD & CDD from EURO-CORDEX


## Ouputs

- Parameters:

  - Graphs comparing the total annual and monthly HDD/CDD between the baseline (BAU) and the scenarios;​
  - KPIs showing the variation between the baseline and the scenario and the modifications in the heating/cooling season length (e.g. percentage increase/decrease).​

- Layers:
- Raster data (TIFF or NetCDF) with mean/median values of HDD/CDD​
  - in raster format (\*.tif)
  - EPSG 3035 projection
  - the resolution depends on the _Tile size_ input parameter.


## Wiki
Further information on the calculation module methodology can be found [here](https://enermaps-wiki.herokuapp.com/en/HeatingCoolingScenarios.md).