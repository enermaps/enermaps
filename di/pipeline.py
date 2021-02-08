import os
from dataflows import Flow, dump_to_path, load, add_computed_field, delete_fields
import requests
import io
import curlify

def get_NEWA():
	"""Retrieves data from NEWA using dataflows"""
	url = "http://opendap.neweuropeanwindatlas.eu/opendap/newa/NEWA_MESOSCALE_ATLAS/2015/NEWA-2015-12-30.nc.nc?PD[0:1:47][2:2][592:1:693][373:1:468],time[0:1:47],height[2:2],west_east[373:1:468],south_north[592:1:693],XLON[592:1:693][373:1:468],XLAT[592:1:693][373:1:468],Times[0:1:47],crs"
	# url = "http://opendap.neweuropeanwindatlas.eu:80/opendap/newa/NEWA_MESOSCALE_ATLAS/2009/NEWA-2009-12-30.nc.nc?PD[0:1:47][2:1:2][0:1:1381][0:1:1597]"
	r = requests.get(url, allow_redirects=True)
	filename = "newa.nc"
	open(filename, 'wb').write(r.content)
	Flow(
        load('newa.nc',format="NetCDF"),
        dump_to_path('data/NEWA', format="geotiff"),
	).process()
	# os.remove(filename)

def post_NEWA():
	"""POST geotiff from NEWA using the API"""
	filename = "data/NEWA/newa_PD_copy.tif"
	url = "http://127.0.0.1:7000/api/geofile/"
	headers = {
	    'accept': 'application/json',
	    'Content-Type': 'multipart/form-data',
	}
	with open(filename, "rb") as f:
		testfile_io = io.BytesIO(f.read())
		test_data = {"file": (f.read(), filename)}
		content = f.read()

	r = requests.post(url,
			data=test_data,
            headers=headers,
            allow_redirects=True
        )
	# print(r.request.headers,r.request.body)
	print(curlify.to_curl(r.request))
	print("")
	print(r.text)

# get_NEWA()
# post_NEWA()


def get_ERA():
	"""Retrieves data from Copernicus using dataflows"""
	Flow(
        load('ERA2.nc',format="raster"),
        dump_to_path('data/ERA', format="geotiff", projection="EPSG:3035"),
	).process()
	# os.remove(filename)

get_ERA()
