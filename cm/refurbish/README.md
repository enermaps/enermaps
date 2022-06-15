# CM - Refurbishment Rate Impact

## Objective

The objective of this CM is to Assess the impact of different building refurbishment scenarios​. With this calculation module you can determine the impact of different refurbish rates under diverse climatic scenarios on building energy demand. Inputs to the module are heating and cooling demand projections (HDD & CDD), RCP scenario, building stock features (U-values and surface areas per building sector, type and age class) and population.

## How it works

This calculation module uses heating and cooling demand projections and building datasets to propose an algorithm-based method for determining building energy demand under diverse climatic scenarios. In the toolbox, user has the option to select the building characteristics, the climatic scenario and the refurbish rate. The building energy demands are determined via estimating the current energy demands based on mean U-values, HDD and CDD. The outputs are tables that show yearly and monthly building heating, cooling and overall demand per building characteristics, climatic scenario and refurbish rate. The calculation module can be used to study the impact of parameters like HDD, CDD and U-values on building energy demand.

### Prerequisite

EnerMaps have to be launched.
If this is not yet the case, see [the general README](../../README.md) to find out how to do so.

Once EnerMaps launched, the frontend should be available on this adress : http://127.0.0.1:7000.

## Inputs

- Parameters:
  - HDD base temperature [_**°C**_]
  - CDD base temperature [_**°C**_]
  - RCP scenario
  - reference year
  - building typology
  - start epoch of construction
  - end epoch of construction
  - percentage of basic refurbished buildings [_**%**_]
  - percentage of advance refurbished buildings [_**%**_]
- Layers:
  - the country-based dataset with the main [building stock data](https://gitlab.com/hotmaps/building-stock/) characteristics for different energy sector provided by the [Hotmaps project](https://www.hotmaps-project.eu/);
  - the [Tabula dataset](https://webtool.building-typology.eu/) is used to assess the [thermal trasmittance](https://gitlab.inf.unibz.it/URS/enermaps/tabula) before and after the basic/advance refurbish activities based on differet building stock archetypes identified on the different building typologies and epoch of construction;
  - the [European population](https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/lau) at municipality level provided by GISCO – the Geographic Information System of the Commission.


## Ouputs

* Monthly building heating demand per building characteristics, climatic scenario and refurbish rate [_**kWh/m2**_]
* Monthly building cooling demand per building characteristics, climatic scenario and refurbish rate [_**kWh/m2**_]
* Monthly building overall demand per building characteristics, climatic scenario and refurbish rate [_**kWh/m2**_]
* Yearly building heating demand per building characteristics, climatic scenario and refurbish rate [_**kWh/m2**_]
* Yearly building cooling demand per building characteristics, climatic scenario and refurbish rate [_**kWh/m2**_]
* Yearly building overall demand per building characteristics, climatic scenario and refurbish rate [_**kWh/m2**_]

## Wiki

Further information on the calculation module methodology can be found [here](https://enermaps-wiki.herokuapp.com/en/Refurbish.md).