"""Acceptance test for the wms,
those test that a set of different call on the wms will not trigger it.
"""
from owslib.wms import WebMapService
wms = WebMapService('http://127.0.0.1:7000/api/wms', version='1.1.1')
print(wms.contents)
