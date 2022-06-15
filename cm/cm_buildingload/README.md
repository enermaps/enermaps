<h1>CM BuildingLoad</h1>

## Table of Contents
* [In a glance](#in-a-glance)
* [Introduction](#introduction)
* [Inputs and outputs](#inputs-and-outputs)
* [Method](#Method)
* [GitHub repositories of this calculation module](#github-repositories-of-this-calculation-module)
* [References](#references)
* [How to cite](#how-to-cite)
* [Authors and reviewers](#authors-and-reviewers)
* [License](#license)
* [Acknowledgement](#acknowledgement)

## In a glance

This calculation module allows users to simulate hourly space heating and cooling demand profiles for a user-configured building in a user-defined location.

[**`To Top`**](#table-of-contents)

## Introduction

The BuildingLoad calculation module takes a different approach to many of the other calculation modules included in EnerMaps (and HotMaps). Rather than focusing on aggregated data for a region, BuildingLoad instead allows users to assess how differing climate conditions and building typologies can affect space heating and cooling demand potential for a specific point (in this case, representing the location for a building). Using the granular climate data provided by Copernicus [1] and typical, country-specific building typologies identified by Tabula [2], BuildingLoad allows users to design a simple residential building and then assess the hourly heating and cooling demands over a specified period. The results from this calculation module are useful for those interested in understanding how regional differences in climate and building standards can affect heating and cooling demand at the building level and can also be used to create a heating/cooling energy demand input file for other modeling activities.

[**`To Top`**](#table-of-contents)

## Inputs and outputs
**Input parameters and layers are:**
* Parameters:
  * *Point on map* to gather latitude and longitude coordinates of building location.
  *	*Gross floor area of external structure* [m<sup>2</sup>], acceptable values: [1-99999 m<sup>2</sup>].
  *	*Number of stories* [-], acceptable values: [1-30].
  *	*Building type* [-], acceptable values: [Multi-family house, Single-family house, Terraced house]
  *	*Construction year* [-], acceptable values: [0 to 9999]
  *	*Set temperature for heating* [°C], acceptable values: [10°C-25°C]
  *	*Set temperature for cooling* [°C], acceptable values: [15°C-30°C]
  *	*Month* [-], acceptable values: [January, February, March, April, May, June, July, August, September, October, November, December]
  *	*Model length* [-], acceptable values: [Month, Year]
  *	*Roof type and orientation* [-], acceptable values: [gable roof, north/south orientation; gable roof, east/west orientation; skillion roof, north orientation; skillion roof, east orientation; skillion roof, south orientation; skillion roof, west orientation; flat roof, horizontal orientation]
  *	*Roof pitch* [°], acceptable values: [0°-90°]
  *	*Wall to floor ratio* [-], acceptable values: [0.5-2]
  *	*Building ratio – length* [-], acceptable values: [1-10]
  *	*Building ratio – width* [-], acceptable values: [1-10]
  *	*Façade orientation* [-], acceptable values: [North, East, South, West]
  *	*Area of door* [-], acceptable values: [1-10 m]
  *	*Coverage of front-facing windows* [%], acceptable values: [0%-99.99%]
  *	*Coverage of rear-facing windows* [%], acceptable values: [0%-99.99%]
  *	*Coverage of left-facing windows* [%], acceptable values: [0%-99.99%]
  *	*Coverage of right-facing windows* [%], acceptable values: [0%-99.99%]
* Layers:
  * Copernicus Climate Data
      * 2m temperature
      *	2m dew point temperature
      *	Surface pressure
      *	Surface Solar Radiation Downwards (SSRD)
      *	Direct solar radiation at the surface (FDIR)
      *	Relative humidity
   * Tabula Building Typology
   		* Note: Not included in the EDMT as a layer

**Output indicators and charts are:**

* Indicators:
  *	*Total heating demand* [_**MWh/year**_] for the selected location/building (based on user selection, either total for the day, week, month, or year)
  *	*Total cooling demand* [_**MWh/year**_] for the selected location/building (based on user selection, either total for the day, week, month, or year)
  *	*Peak heating demand* [_**MWh/year**_] for the selected location/building
  *	*Peak cooling demand* [_**MWh/year**_] for the selected location/building
* Charts:
  *	Graph of *hourly heating demand* for the selected location/building (based on user selection, either over the course of a day, week, month, or year)
  *	Graph of *hourly cooling demand* for the selected location/building (based on user selection, either over the course of a day, week, month, or year)
  
[**`To Top`**](#table-of-contents)

## Method

### Calculation module components
The calculation module takes the user inputs and applies the calculation procedure described in ISO 13790:2008 [3] to simulate space heating and cooling demand for the building. The inputs/parameters (described below) are used to define the building while the location of the building is used to generate the appropriate climate data assessing the outdoor temperature and solar radiation.

*Internal gains*: For simplification, typical occupancy-related data for residential buildings was used to estimate internal gains. Internal heat gains vary based on the time of day and day of the week.

*Solar gains*: Solar gains are calculated using the Perez diffuse irradiance model [4]. The solar radiation and resulting heat gains are calculated for each building element based on the climatic conditions for the given hour and the area, thermal resistance, orientation, azimuth, etc. of the building element.

*Heat demand calculation*: The heat demand calculation utilizes a Crank-Nicholson scheme to assess space heating or cooling demand for each hour. Heating needs are based on the internal air temperature which is a function of the outside air temperature and heat transfers through ventilation and both opaque and glazed elements and heat flows to medium, air, and internal surfaces.

*Stories*: The user must define the number of stories of the building. All stories are assumed to be the same dimensions (i.e., equal height and floor area shape). 

*Gross internal and external floor area*: Gross external floor area (GEFA) is requested for input from the user. Gross internal floor area (GIFA) is calculated by multiplying GEFA by 0.85 (a correction parameter utilized by Tabula for its calculation of GIFA) and by the number of stories.

*Conditioned floor area*: For simplification, conditioned floor area (the area of internal spaces that are to stay within the upper and lower comfort boundaries) is set as equal to the gross internal floor area. This assumes that all internal space is conditioned equally.

*Roof pitch*: The user has the option of defining the roof pitch which is used to define the roof tilt and assess the radiation form factor of the roof.

*Roof area*: Roof area is calculated by multiplying the floor area of the medium by the cosine of the provided roof pitch. For simplification purposes, information on roof overhang is not collected and therefore not included in the roof area calculation. 

*Roof azimuth*: Roof azimuth (or two azimuths for gable roofs) is assigned based on the building orientation.

*External wall area*: External walls are calculated using the proportion of Tabula reference building volume to gross external floor area for the selected building class, type, and country. This proportion is applied to the gross external floor area provided by the user to approximate the assessed building’s wall area.

*Individual external wall dimensions*: Ignoring the roof, the building structure is assumed to be a rectangular prism with two sets of two parallel vertical sides (or cubic, with all vertical sides being equal). The user has the option to set the dimensions of the building (the length and width of the building, with the width being the façade side and back of building and the length being the sides of the building).

*Orientation of external walls*: The user is requested to optionally define the orientation of the building by stating the orientation of the façade side of the building (the building “front” where the door is located). 

*External wall azimuths*: External wall azimuths are assigned using the building orientation.

*Window area*: Window area is a function of the external wall area. Users are given the option to define how much of each external wall is covered by glazed surfaces (e.g. windows). This proportion is multiplied by each external wall area to calculate the area of glazed surfaces for each side.

*Door area*: The user has the option of defining the area of the door on the façade side. The model assumes only one door, which is treated as a glazed element.

### Assumption and limitations
As mentioned in the “Calculation module components” subsection of this wiki, there are many assumptions that limit the usefulness of the model for certain uses. The simplified nature of the model benefits by being compact enough to be implemented in a webtool such as the EDMT, however this lack of complexity comes at the cost of overall accuracy. Users should be mindful that all generated results are estimates to provide an impression rather than a simulation of full, real-world conditions. 

Please note that the calculation time for model lengths larger than a single day may be quite long (up to 12 minutes for annual length).

[**`To Top`**](#table-of-contents)

## GitHub repositories of this calculation module

[**`To Top`**](#table-of-contents)

## References

[1] Hersbach, H., Bell, B., Berrisford, P., Biavati, G., Horányi, A., Muñoz Sabater, J., Nicolas, J., Peubey, C., Radu, R., Rozum, I., Schepers, D., Simmons, A., Soci, C., Dee, D., Thépaut, J-N. ERA5 hourly data on single levels from 1979 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS), 2018 10.24381/cds.adbb2d47

[2] TABULA WebTool. http://webtool.building-typology.eu/#bm

[3] ISO. EN ISO 13790:2008 thermal performance of buildings - calculation of energy use for space heating and cooling, 2008.

[4] Perez, R., Stewart, R., Seals, R., and Guertin, T. The development and verification of the Perez diffuse radiation model, 1988.

[**`To Top`**](#table-of-contents)

## How to cite

Eric Wilczynski, [EURAC Research](https://www.eurac.edu), in EnerMaps Wiki, BuldingLoad Calculation Module, December 2021.

[**`To Top`**](#table-of-contents)

## Authors and reviewers
This page was written by Eric Wilczynski (**[EURAC Research](https://www.eurac.edu)**).

This page was reviewed Simon Pezzutto (**[EURAC Research](https://www.eurac.edu)**) and XXX.

[**`To Top`**](#table-of-contents)

## License

Copyright © 2021: Eric Wilczynski

Creative Commons Attribution 4.0 International License

This work is licensed under a Creative Commons CC BY 4.0 International License.

SPDX-License-Identifier: CC-BY-4.0

License-Text: https://spdx.org/licenses/CC-BY-4.0.html

[**`To Top`**](#table-of-contents)

## Acknowledgement

We would like to convey our deepest appreciation to the Horizon 2020 EnerMaps Project (Grant Agreement number 884161), which provided the funding to carry out the present investigation.

[**`To Top`**](#table-of-contents)


<!--- Links -->
[database]: database.md
[unpivoting]: images/di-unpivoting.png
