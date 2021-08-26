# References 
This calculation module (CM) was originally written as part of the 
[HotMaps](https://www.hotmaps-project.eu/) project.

The documentation that was done for this first version can be found on
[this section](https://wiki.hotmaps.eu/en/CM-District-heating-potential-areas-user-defined-thresholds) 
of the HotMaps wiki project.

# Requirements
As indicated in the CM documentation, the dependencies specific 
to a CM are in the folder dedicated to this CM under the name 
`requirements.txt`. 

For this CM, one of the dependencies, GDAL, is not in this file.
Indeed, the installation is done rectly through command line in 
the Dockerfile.


# Goal of the calculation module
This CM calculates district heating potential within the selected region using 2 threshold values: 
* Minimum heat demand in each hectare, 
* Minimum heat demand in a DH area. 

# Processing

## Set the parameters
The CM input parameters are :
* Minimum heat demand in each hectare [MWh/ha]: a value between 0 and 1000
* Minimum heat demand in a district heating (DH) area [GWh/year]: a value between 0 and 500
* Heat density map: a raster with 1-hectare resolution and demand in MWh
* A study area: given directly from the interface

## Clip the raster
The CM clip the raster according to the study area.
The resulting raster will be used for the rest of the process

## Get areas and potentials

### Demand in hectare 
The first filter applied to the layer will set to zero 
the value of all pixels below a threshold value.

The threshold value is the minimum heat demand in each hectare.

### Demand in DH
The studied layer contains one or more areas where the potential is null.
The CM will then apply successively a binary dilatation 
(see [scipy page](https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.morphology.binary_dilation.html) 
for more information) and erosion operation
(see [scipy page](https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.ndimage.morphology.binary_erosion.html) 
for more information) to obtain the final layer.

Then, the CM sum values of the remaining pixels zone by zone the value.
If the sum of a zone is less than a given threshold, 
the pixel values defining this zone are being  to zero. 

The threshold value is the minimum heat demand in a DH area.

## Return results
The CM returns:
- indicators: 
    * Total district heating potential (GWh)
    * Total heat demand (GWh)
    * Potential share of district heating from total demand in selected zone (%)
- graph:
    * A bar chart of the potential of the selected areas
- raster:
    * This layer contains all the areas that have been retrained after processing.