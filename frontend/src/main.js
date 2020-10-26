var map = L.map("map").setView([51.505, -0.09], 13);

var base0 = L.tileLayer.wms("http://ows.mundialis.de/services/service?", {
  layers: "TOPO-OSM-WMS",
});
map.addLayer(base0);
var base_map = {};
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
layer_control = L.control.layers(base_map, {})
layer_control.addTo(map);
$.ajax({
	url: "/api/geofile"
}).done(function(data){
console.log("layers are :", data.files);
for (const layer_index in data.files) {
  const layer_name = data.files[layer_index];
  const layer = L.tileLayer.wms(
    "/api/wms?",
    {
      transparent: "true",
      layers: layer_name,
      format: "image/png",
    }
  );
  layer.is_overlay = true;
  layer_control.addOverlay(layer, layer_name);
	console.log("adding ", layer);
}
});

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

$.ajax({
  dataType: "json",
  url: "/api/cm/0/task/0",
  success: function( result ) {

      var result_js = JSON.parse(JSON.stringify(result));
      var result_js_labels = Object.keys(result_js);
      var result_js_values = Object.values(result_js);

      var backgroundColor_array = [];
      var i;
      for(i=0; i < result_js_values.length; i++){
          backgroundColor_array[i] = "rgba("+ Math.floor(Math.random()*256) +","+Math.floor(Math.random()*256)+","+ Math.floor(Math.random()*256)+",0.2)"
      }

      var ctx = document.getElementById('myChart').getContext('2d');
      var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: result_js_labels,
            datasets: [{
                label: 'fake data output ',
                data: result_js_values,
                backgroundColor: backgroundColor_array,
                borderColor: backgroundColor_array,
                borderWidth: 2}]
            },
        options: {
            title : {
                display : true,
                text : ['Fake outputs grpah', 'Just for example'],
                fontSize :20},
            legend: {display : false}
        }
      })
  }});




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
