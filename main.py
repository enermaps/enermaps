import os
import io

from flask import Flask, safe_join, send_file, Response
from flask_restx import Api, Resource
from werkzeug.datastructures import FileStorage
import mapnik

app = Flask(__name__)
app.config["UPLOAD_DIR"] = "/tmp/upload_dir"
api = Api(app)

def get_user_upload(user="user"):
    user_dir = safe_join(app.config["UPLOAD_DIR"], user)
    try:
        os.makedirs(user_dir)
    except FileExistsError:
        pass
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
        safe_join(get_user_upload(), uploaded_file.filename)
        return {"status": "upload succeeded"}


@api.route("/geofile/<string:path>")
class GeoFile(Resource):
    def get(self, path):
        file_path = safe_join(get_user_upload(), path)
        with open(file_path, 'rb') as f:
            return send_file(f, attachment_filename=path)

@api.route("/tile/<string:path>/<int:zoom>/<int:x>/<int:y>")
class TileServer(Resource):
    @api.produces(['image/png'])
    def get(self, path, zoom, x, y):
        image = mapnik.Image(600, 300)
        mp = mapnik.Map(600, 300)
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

if __name__ == "__main__":
    app.run(debug=True)
