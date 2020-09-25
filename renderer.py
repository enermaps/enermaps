import mapnik
import sys
from collections import namedtuple

TILE_SIZE = 256
S = namedtuple("S", ['x', 'y'])

def get_bbox():
    #bbox_dim = (9.843750, 47.040182, 15.468750, 49.837982, )
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
        #mp.srs = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
        #mp.background = mapnik.Color('steelblue')
        lyr = mapnik.Layer('gdal')
        lyr.datasource = mapnik.Gdal(file=layer)
        lyr.styles.append('My Style')
        mp.background = mapnik.Color('transparent')
        s = mapnik.Style()
        r = mapnik.Rule()
        r.symbols.append(mapnik.RasterSymbolizer())
        s.rules.append(r)
        mp.append_style('My Style',s)
        #mp.layers.append(lyr)
        mp.zoom_to_box(lyr.envelope())
        print(lyr.envelope())
        #mp.zoom_to_box(get_bbox())
        mapnik.render(mp, image)
        image.save("tile_{!s}_{!s}_{!s}.png".format(x, y, z))

if __name__ == "__main__":
    file_path = sys.argv[1]
    z = int(sys.argv[2])
    x = int(sys.argv[3])
    y = int(sys.argv[4])
    render_tile(file_path, x,y,z)
