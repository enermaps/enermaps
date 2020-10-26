var map = L.map("map").setView([51.505, -0.09], 13);

var baseLayer = new L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
})
map.addLayer(baseLayer);
var base_map = {};
const workspace_name = "enermaps";
const layer_name = "nuts";
for (var nuts_index = 0; nuts_index < 4; nuts_index++) {
  base_map[layer_name.toUpperCase() + " " + nuts_index] = L.tileLayer.nutsLayer(
    "/api/wms?",
    {
      transparent: "true",
      layers: "nuts" + nuts_index + ".zip",
      format: "image/png",
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
      for(i=0; i < result_js_values.length; i++) {
          backgroundColor_array[i] = "rgba("+ Math.floor(Math.random()*256) +","+Math.floor(Math.random()*256)+","+ Math.floor(Math.random()*256)+",0.2)"
      };

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
                text : ['Graph 1 - NUMBER ONE', 'Just for example'],
                fontSize :20},
            legend: {display : true},
            scales :{
                xAxes :[{
                    scaleLabel:{
                        display: true,
                        labelString:'X UNIT'}}],
                yAxes :[{
                    scaleLabel:{
                        display: true,
                        labelString:'y UNIT'}}]
                }}
      });

      for(i=0; i < result_js_values.length; i++) {
          backgroundColor_array[i] = "rgba("+ Math.floor(Math.random()*256) +","+Math.floor(Math.random()*256)+","+ Math.floor(Math.random()*256)+",0.2)"
      };
      var ctx2 = document.getElementById('myChart2').getContext('2d');
      var myChart2 = new Chart(ctx2, {
        type: 'line',
        data: {
            labels: result_js_labels,
            datasets: [{
                label: 'fake data output ',
                data: result_js_values,
                backgroundColor : "rgb(154, 6, 71,0.2)",
                pointRadius : 2
                }]
            },
        options: {
            title : {
                display : true,
                text : ['Graph 2 - NUMBER TWO', 'Just for example'],
                fontSize :20},
            legend: {display : true}
        }
      });

      for(i=0; i < result_js_values.length; i++) {
          backgroundColor_array[i] = "rgba("+ Math.floor(Math.random()*256) +","+Math.floor(Math.random()*256)+","+ Math.floor(Math.random()*256)+",0.2)"
      };
      var ctx3 = document.getElementById('myChart3').getContext('2d');
      var myChart3 = new Chart(ctx3, {
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
                text : ['Graph 3 - NUMBER THREE', 'Just for example'],
                fontSize :20},
            legend: {display : true}
        }
      });

      for(i=0; i < result_js_values.length; i++) {
          backgroundColor_array[i] = "rgba("+ Math.floor(Math.random()*256) +","+Math.floor(Math.random()*256)+","+ Math.floor(Math.random()*256)+",0.2)"
      };
      var ctx4 = document.getElementById('myChart4').getContext('2d');
      var myChart4 = new Chart(ctx4, {
        type: 'horizontalBar',
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
                text : ['Graph 4 - NUMBER FOUR', 'Just for example'],
                fontSize :20},
            legend: {display : true}
        }
      });

  }});

$(function(){
    $("#graph_hider").click(function(){
        if( $(".container").is(':visible') ){
            $(".container").hide(1000, function(){
                $("#graph_hider").text("Show graph");})}
        if( $(".container").is(':hidden') ){
            $(".container").show(10);
            $("#graph_hider").text("Hide graph")}
    })
})



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
