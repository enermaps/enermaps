import mapnik
import sys
from collections import namedtuple
import gdal
gdal.UseExceptions()    # Enable exceptions

TILE_SIZE = 3026
S = namedtuple("S", ['x', 'y'])

def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom # : the number of tiles
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

def get_bbox():
    bbox_dim = (9.843750, 47.040182, 15.468750, 49.837982, )
    #bbox_dim = (8.3,48.95,8.5,49.05)
    #bbox_dim = (0,48.95,0,49.05)
    if hasattr(mapnik, 'mapnik_version') and mapnik.mapnik_version() >= 800:
        bbox = mapnik.Box2d(*bbox_dim)
    else:
        bbox = mapnik.Envelope(*bbox_dim)
    return bbox
    
def render_tile(layer, z, x, y):
        image = mapnik.Image(TILE_SIZE, TILE_SIZE)
        mp = mapnik.Map(TILE_SIZE, TILE_SIZE)
        mp.srs = "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over"
        #mp.background = mapnik.Color('steelblue')
        lyr = mapnik.Layer('gdal')
        #lyr.srs = "+proj=laea +lat_0=52 +lon_0=10 +x_0=4321000 +y_0=3210000 +ellps=GRS80 +units=m +no_defs"
        lyr.srs = "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over"
        #band = dataset.GetRasterBand(1)
        lyr.datasource = mapnik.Gdal(file=layer, band=1)#, band=20)
        lyr.styles.append('My Style')
        #mp.background = mapnik.Color('steelblue')
        s = mapnik.Style()
        r = mapnik.Rule()
        rs = mapnik.RasterSymbolizer()
        rs.colorizer = mapnik.RasterColorizer(mapnik.COLORIZER_DISCRETE, mapnik.Color(0, 0, 0, 0))
        rs.colorizer.add_stop(-417, mapnik.Color(0, 0, 0))
        rs.colorizer.add_stop(68, mapnik.Color(255, 255, 255))
        rs.colorizer.add_stop(234, mapnik.Color(255, 0, 0))
        rs.colorizer.add_stop(461, mapnik.Color(0, 0, 255))
        rs.colorizer.add_stop(720, mapnik.Color(0, 255, 0))
        r.symbols.append(rs)
        s.rules.append(r)
        mp.append_style('My Style',s)
        mp.layers.append(lyr)
        #mp.zoom_to_box(lyr.envelope())
        print(lyr.envelope())
        mp.zoom_to_box(get_bbox())
        mapnik.render(mp, image)
        image.save("tile_{!s}_{!s}_{!s}.png".format(z, x, y))

if __name__ == "__main__":
    file_path = sys.argv[1]
    z = int(sys.argv[2])
    x = int(sys.argv[3])
    y = int(sys.argv[4])
    render_tile(file_path, x,y,z)
