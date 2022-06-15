# CM - District Heating Economic Assessment

With this calculation module, you can determine potential district heating areas based on a simplified assessment of the distribution and service pipeline costs. Inputs to the module are heat demand and gross floor area density maps, development of connection rates, depreciation time, interest rate and a threshold for the accepted heat distribution costs.

## How it works

This calculation module (CM) uses a heat density map (HDM) and a gross floor area density map to propose a GIS-based method for determining potential DH areas with specific focus on district heating (DH) grid costs. In the EnerMaps Data Management Tool (EDMT), the default datasets used by the CM, namely [heat demand density map](https://gitlab.com/hotmaps/heat/heat_tot_curr_density) and the [gross floor area density map](https://gitlab.com/hotmaps/gfa_tot_curr_density) are provided.
The DH areas are determined via performing sensitivity analyses on the HDM under consideration of predefined upper bound of the average distribution costs. The CM also calculates the length of distribution pipes as well as service pipes. Please note that services pipes are those pipes that connect distribution grid to the buildings. Therre is no dimension boundary for distinguishing between service pipes and distribution pipes. Distinguishing between these two is done emperically. The outputs are GIS layers that illustrate areas that are economically viable for the construction of DH system as well as a set of indicators. The calculation module can be used to study the impact of parameters like grid costs ceiling and market share on potential and on expansion and extension of the DH systems.

## Prerequisite

EnerMaps has to be launched.
If this is not yet the case, see [the general README](../../README.md) to find out how to do so.

Once EnerMaps launched, the frontend should be available on this adress : http://127.0.0.1:7000.

The API key of the PostgREST API must be placed in a text file `cm/heatlearn/API_KEY.txt`.

## Inputs

- Parameters:
  - Country: used for obtaining default construction cost **constant** as well as construction cost **coefficient**. It is possible to use construction cost factors of one country for the calculation corresponding to another country. If user-defined construction cost factors are provided, this parameter will not be used.
  - Select output layer for visualisation: the current version of EDMT can visualize one ouptut layer at each run. With this parameter, the user tells the CM which output layer should be visualized.
  - Grid cost ceiling in _**EUR/MWh**_: In potential DH areas, the distribution grid cost may not exceed this defined distribution grid cost ceiling. Values range [10-100 EUR/MWh]
  - Minimum heat demand in hectare _**MWh/(ha*year)**_: Criteria for identifying a potential DH area. Values range [20-1000000000 MWh/(ha*year)]
  - Minimum heat demand in a potential DH area _**GWh/year**_: Criteria for identifying a potential DH area. Values range [1-1000000000 GWh/year]
  - First year of investment
  - Last year of investment: determines in how many years you should reach the targeted DH market share.
  - Starting district heating market share: A value between zero and one [0-1] showing the current state in the selected area.
  - Final district heating market share: A value between zero and one [0-1] showing the expected market share in the last year of investment.
  - Depreciation period in _**years**_: higher depreciation time makes the overall cost lower as your system will last longer and serves more. Values range [1-200 years]
  - Interest rate [0-1]
  - Use country specific values for both construction cost constant and coefficient: True for default values and False for user-defined values
  - Construction cost **constant** in _**EUR/m**_ as well as Construction cost **coefficient** in _**EUR/m<sup>2</sup>**_: based on reference [[1](#references)]. Values range [0.1-10000 EUR/m] and [0.1-10000 EUR/m<sup>2</sup>] respectively.
- Layers:
  - Heat density map and gross floor area density map:
    - in raster format (\*.tif)
    - with 1 hectare resolution
    - demand densities in _**MWh/ha**_ and gross floor area densities in _**m<sup>2</sup>/ha**_

## Outputs

- Parameters:
  - Starting connection rate in _**%**_
  - End connection rate in _**%**_
  - Grid cost ceiling in _**EUR/MWh**_
  - Start year - Heat demand in DH areas in _**GWh**_
  - End year - Heat demand in areas in _**GWh**_
  - Start year - Heat coverage by DH areas in _**GWh**_
  - End year - Heat coverage by DH areas in _**GWh**_
  - Total supplied heat by DH over the investment period in _**TWh**_
  - Average DH grid cost in DH areas in _**EUR/MWh**_
  - Total DH distribution grid length in _**km**_
  - Total DH service pipe length in _**km**_
- Layers:
  - Specific network costs
  - DH areas 


## Wiki

Further information on the calculation module methodology can be found [here](https://enermaps-wiki.herokuapp.com/en/DH-economic-assessment.md).