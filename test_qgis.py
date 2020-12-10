from qgis.core import *

# supply path to where is your qgis installed
app = QgsApplication([], True)
QgsApplication.setPrefixPath("/usr", True)

# load providers
QgsApplication.initQgis()
urlWithParams = 'url=http://www.geostore.com/OGC/OGCInterface?SESSIONID=-2049535737&INTERFACE=ENVIRONMENT&version=1.3.0&service=WMS&request=GetLegendGraphic&sld_version=1.1.0&layer=eainspire2011-wms-nat_floodzone2_inspire&format=image/png&STYLE=default'
rlayer = QgsRasterLayer(urlWithParams, 'EA Flood Zone 2', 'wms')
rlayer.isValid()
QgsProject.instance().addMapLayer(rlayer)
