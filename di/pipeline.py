import os
from dataflows import Flow, dump_to_path, load, add_computed_field, delete_fields
import requests
import io
# import curlify

def get_NEWA():
	"""Retrieves data from NEWA using dataflows"""
	url = "http://opendap.neweuropeanwindatlas.eu/opendap/newa/NEWA_MESOSCALE_ATLAS/2015/NEWA-2015-12-30.nc.nc?PD[0:1:47][2:2][592:1:693][373:1:468],time[0:1:47],height[2:2],west_east[373:1:468],south_north[592:1:693],XLON[592:1:693][373:1:468],XLAT[592:1:693][373:1:468],Times[0:1:47],crs"
	r = requests.get(url, allow_redirects=True)
	filename = "newa.nc"
	open(filename, 'wb').write(r.content)
	Flow(
        load('newa.nc',format="NetCDF"),
        dump_to_path('data/NEWA', format="geotiff", projection="EPSG:3035"),
	).process()
	os.remove(filename)

def post_NEWA():
	"""POST geotiff from NEWA using the API"""
	filename = "data/NEWA/newa_PD.tif"
	url = "http://127.0.0.1:7000/api/geofile/"
	with open(filename, "rb") as f:
		testfile_io = io.BytesIO(f.read())
		test_data = {"file": (f.read(), "test.tif")}
		files={'files': f}
		r = requests.post(url, files=files,
	            headers={"content_type":"multipart/form-data"},
	        )
		print(r.request.headers,r.request.body)
		# print(curlify.to_curl(r.request))
		print(r.text)

get_NEWA()
post_NEWA()