import gdal
import osr
from mapnik import Projection


def proj4_from_geotiff(path):
    raster = gdal.Open(path)
    prj = raster.GetProjection()
    prj = prj.strip()
    if not prj:
        return ""
    srs = osr.SpatialReference(wkt=prj)

    return srs.ExportToProj4()


class CRS:
    """This class is an helper to manipulate coordinate on some CRS projection, the x and y coordinate are sometime swapped when doing a projection from one CRS to another, this class helps this process.
    """

    def __init__(self, namespace, code):
        self.namespace = namespace.lower()
        self.code = int(code)
        self.proj = None

    def __repr__(self):
        return "%s:%s" % (self.namespace, self.code)

    def __eq__(self, other):
        if str(other) == str(self):
            return True
        return False

    def inverse(self, x, y):
        if not self.proj:
            self.proj = Projection("+init=%s:%s" % (self.namespace, self.code))
        return self.proj.inverse(Coord(x, y))

    def forward(self, x, y):
        if not self.proj:
            self.proj = Projection("+init=%s:%s" % (self.namespace, self.code))
        return self.proj.forward(Coord(x, y))
