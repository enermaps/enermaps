import os
import io
from flask import Flask, safe_join, send_file, Response, send_from_directory, request
from PIL import Image
from flask_restx import Api, Resource
from werkzeug.datastructures import FileStorage
from marshmallow import Schema, fields
import mapnik

app = Flask(__name__)
app.config["UPLOAD_DIR"] = "/tmp/upload_dir"
app.config["TILE_DIR"] = "/tmp/tiles"
api = Api(app)

def get_user_upload(user="user"):
    user_dir = safe_join(app.config["UPLOAD_DIR"], user)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

def get_tile_dir(user="user"):
    user_dir = safe_join(app.config["TILE_DIR"], user)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)

@api.route("/geofile")
class GeoFiles(Resource):
    def get(self):
        user_dir = get_user_upload()
        files = os.listdir(user_dir)
        return {"files": files}

    @api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance
        output_filepath = safe_join(get_user_upload(), uploaded_file.filename)
        uploaded_file.save(output_filepath)
        return {"status": "upload succeeded"}

MIN_ZOOM = 1
MAX_ZOOM = 7

def generate_tiles(geofile_path):
    GDAL2Tiles('--leaflet',  'geofile_path', '-z', '{!s}-{!s}'.join(MIN_ZOOM, MAX_ZOOM)), geofile_path, 

@api.route("/geofile/<string:path>")
class GeoFile(Resource):
    def get(self, path):
        file_path = safe_join(get_user_upload(), path)
        with open(file_path, 'rb') as f:
            return send_file(f, attachment_filename=path)

    def put(self, path):
        file_path = safe_join(get_user_upload(), path)
        with open(file_path, 'rb') as f:
            return send_file(f, attachment_filename=path)

    @api.expect(upload_parser)
    def put(self):
        args = upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance
        output_filepath = safe_join(get_user_upload(), uploaded_file.filename)
        uploaded_file.save(output_filepath)
        return {"status": "upload succeeded, file updated"}

@api.route("/geofile/<string:path>")
class RasterStats(Resource):
    pass

def parse_layers(normalized_params):
    for layer in normalized_params['layers']:
        return layer

@api.route("/geofile/tile/<string:path>")
class PreviewTileServer(Resource):
    @api.produces(['image/png'])
    def get(self, path):
        normalized_args = {k.lower(): v for k, v in request.args.items()}
        projection = request.args.get("srs")
        height = int(request.args.get("height"))
        height = int(request.args.get("width"))
        layers = parse_layers(normalized_args)
        image = mapnik.Image(width, width)

        mp = mapnik.Map()
        mp.background = mapnik.Color('steelblue')
        lyr = mapnik.Layer('overlay')
        file_path = safe_join(get_user_upload(), path)
        lyr.datasource = mapnik.Gdal(file=file_path)
        srs_string = ""
        #lyr.styles.append('My Style')
        mp.background = mapnik.Color('transparent')
        s = mapnik.Style()
        r = mapnik.Rule()
        r.symbols.append(mapnik.RasterSymbolizer())
        s.rules.append(r)
        mp.append_style('My Style',s)
        #mp.zoom_to_box(lyr.envelope())
        mapnik.render(mp, image)
        return Response(image.tostring('png'), mimetype='image/png')

@app.route("/test")
def test():
    print(request.args)
    return ""

class CRS:
    def __init__(self, namespace, code):
        self.namespace = namespace.lower()
        self.code = int(code)
        self.proj = None

    def __repr__(self):
        return '%s:%s' % (self.namespace, self.code)

    def __eq__(self, other):
        if str(other) == str(self):
            return True
        return False

    def inverse(self, x, y):
        if not self.proj:
            self.proj = Projection('+init=%s:%s' % (self.namespace, self.code))
        return self.proj.inverse(Coord(x, y))

    def forward(self, x, y):
        if not self.proj:
            self.proj = Projection('+init=%s:%s' % (self.namespace, self.code))        
        return self.proj.forward(Coord(x, y))

def to_bbox(*bbox_dim):
    if hasattr(mapnik, 'mapnik_version') and mapnik.mapnik_version() >= 800:
        bbox = mapnik.Box2d(*bbox_dim)
    else:
        bbox = mapnik.Envelope(*bbox_dim)
    return bbox

@api.route("/wms")
class WMS(Resource):

    def get(self):
        normalized_args = {k.lower(): v for k, v in request.args.items()}
        print(normalized_args)
        projection = request.args.get("srs").lower()
        #validate projection
        print(request.args)
        height = int(request.args["height"])
        width = int(request.args['width'])
        #layers = parse_layers(normalized_args)
        layer = mapnik.Layer('hillshade')
        layer.srs = "+proj=laea +lat_0=52 +lon_0=10 +x_0=4321000 +y_0=3210000 +ellps=GRS80 +units=m +no_defs"
        layer.datasource = mapnik.Gdal(file='/home/malik/Scribble/OGCServer/tiff/hotmaps-heat_tot_curr_density.tif')
        #layer.minimum_scale_denominator

        s = mapnik.Style()
        r = mapnik.Rule()
        r.symbols.append(mapnik.RasterSymbolizer())
        s.rules.append(r)

        mp = mapnik.Map(width, height, '+init=' + projection)
        mp.append_style('My Style',s)
        layer.styles.append('My Style')
        mp.layers.append(layer)
        #mp.background_color = 'steelblue'
        bbox = [float(extrema) for extrema in normalized_args['bbox'].split(',')]
        mp.zoom_to_box(to_bbox(bbox[0], bbox[1], bbox[2], bbox[3]))
        image = mapnik.Image(width, height)
        #image_format = im.to 
        mapnik.render(mp, image)
            
        #with io.BytesIO() as output:
        #    image.save(output, format="GIF")
        return Response(image.tostring('png'), mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
