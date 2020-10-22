var map = L.map("map").setView([51.505, -0.09], 13);

var base0 = L.tileLayer.wms("http://ows.mundialis.de/services/service?", {
  layers: "TOPO-OSM-WMS",
});
map.addLayer(base0);
var base_map = {};
$.ajax({
	url: "http://127.0.0.1:5000/geofile"
}).done(function(data){
	console.log("layers are :", data);
})
var layer_names = [
  "SWISSALTI3D_10_TIFF_CHLV95_LN02_2600_1196.tif",
  "reformatted.tif",
];
var layers = {};
for (const layer_index in layer_names) {
  const layer_name = layer_names[layer_index];
  const workspace_name = layer_name.split(":")[0];
  layers[layer_name] = L.tileLayer.wms(
    "http://127.0.0.1:5000/wms?",
    {
      transparent: "true",
      layers: layer_name,
      format: "image/png",
    }
  );
  layers[layer_name].is_overlay = true;
}
const workspace_name = "enermaps";
const layer_name = "nuts";
for (var nuts_index = 0; nuts_index < 4; nuts_index++) {
  base_map[layer_name.toUpperCase() + " " + nuts_index] = L.tileLayer.nutsLayer(
    "http://127.0.0.1:2000/geoserver/" + workspace_name + "/wms?",
    {
      transparent: "true",
      layers: "enermaps:nuts",
      format: "image/png",
      cql_filter: "stat_levl_ =" + nuts_index + " AND year='2013-01-01'",
    }
  );
}
base_map["LAU"] = L.tileLayer.nutsLayer(
  "http://127.0.0.1:2000/geoserver/enermaps/wms?",
  {
    transparent: "true",
    layers: "enermaps:tbl_lau1_2",
    format: "image/png",
  }
);

var drawingLayer = new L.DrawingLayer();
//map.addLayer(editableLayers);
base_map["Draw"] = drawingLayer;
L.control.layers(base_map, layers).addTo(map);

map.addControl(
  new L.Control.Search({
    url: "https://nominatim.openstreetmap.org/search?format=json&q={s}",
    jsonpParam: "json_callback",
    propertyName: "display_name",
    propertyLoc: ["lat", "lon"],
    marker: false,//L.circleMarker([0, 0], { radius: 30 }),
    autoCollapse: true,
    autoType: false,
    minLength: 2,
  })
);

//map.on('draw:created', function(e) {
//  var type = e.layerType,
//    layer = e.layer;
//
//  if (type === 'marker') {
//    layer.bindPopup('A popup!');
//  }
//
//  editableLayers.addLayer(layer);
//});
