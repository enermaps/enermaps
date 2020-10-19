import os
import io

from flask import Flask, safe_join, send_file, Response, send_from_directory
from flask_restx import Api, Resource
from werkzeug.datastructures import FileStorage
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

@api.route("/geofile/stats/<string:type>")
class RasterStats(Resource):
    pass
    
@api.route("/geofile/tile/<string:path>")
class PreviewTileServer(Resource):
    @api.produces(['image/png'])
    def get(self, path):
        image = mapnik.Image(3134, 3134)
        mp = mapnik.Map(3134, 3134)
        #mp.background = mapnik.Color('steelblue')
        lyr = mapnik.Layer('world')
        file_path = safe_join(get_user_upload(), path)
        lyr.datasource = mapnik.Gdal(file=file_path)
        lyr.styles.append('My Style')
        mp.background = mapnik.Color('transparent')
        s = mapnik.Style()
        r = mapnik.Rule()
        r.symbols.append(mapnik.RasterSymbolizer())
        s.rules.append(r)
        mp.append_style('My Style',s)
        mp.layers.append(lyr)
        mp.zoom_to_box(lyr.envelope())
        mapnik.render(mp, image)
        return Response(image.tostring('png'), mimetype='image/png')


@api.route("/geofile/tile/<string:path>/<int:zoom>/<int:x>/<int:y>")
class TileServingServer(Resource):
    @api.produces(['image/png'])
    def get(self, path, zoom, x, y):
        tile_dir = safe_join(get_tile_dir(user=""), path)
        tile_file = safe_join(str(zoom), str(x), str(y) + '.png')
        return send_from_directory(tile_dir, tile_file)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
