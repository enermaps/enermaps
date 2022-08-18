# CM - Building Heating and Cooling Load


## Objective
This calculation module (CM) allows users to simulate hourly space heating and cooling demand profiles for a user-configured building in a user-defined location.


## How it works

The calculation module Building Heating and Cooling Load takes a different approach to many of the other calculation modules included in EnerMaps (and HotMaps). 
Rather than focusing on aggregated data for a region, this CM allows users to assess how differing climate conditions and building typologies can affect 
space heating and cooling demand potential for a specific point (in this case, representing the location for a building). 
Using the granular climate data provided by Copernicus and typical, country-specific building typologies identified by Tabula, 
the CM allows users to design a simple residential building and then assess the hourly heating and cooling demands over a specified period. 
The results from this calculation module are useful for those interested in understanding how regional differences in climate and building standards 
can affect heating and cooling demand at the building level and can also be used to create a heating/cooling energy demand input file for other modeling activities.

## Prerequisite

EnerMaps has to be launched.
If this is not yet the case, see [the general README](../../README.md) to find out how to do so.

Once EnerMaps launched, the frontend should be available on this adress : http://127.0.0.1:7000.

The API key of the PostgREST API must be placed in a text file `cm/heatlearn/API_KEY.txt`.

## Inputs

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

## Outputs

* Indicators:
  *	*Total heating demand* [_**MWh/year**_] for the selected location/building (based on user selection, either total for the day, week, month, or year)
  *	*Total cooling demand* [_**MWh/year**_] for the selected location/building (based on user selection, either total for the day, week, month, or year)
  *	*Peak heating demand* [_**MWh/year**_] for the selected location/building
  *	*Peak cooling demand* [_**MWh/year**_] for the selected location/building
* Charts:
  *	Graph of *hourly heating demand* for the selected location/building (based on user selection, either over the course of a day, week, month, or year)
  *	Graph of *hourly cooling demand* for the selected location/building (based on user selection, either over the course of a day, week, month, or year)


## Wiki

Further information on the calculation module methodology can be found [here](https://enermaps-wiki.herokuapp.com/en/CM%20Building%20Heat%20Load.md).