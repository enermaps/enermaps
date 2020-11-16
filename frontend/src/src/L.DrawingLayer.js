import "leaflet-draw/dist/leaflet.draw.js";
import "leaflet-draw/dist/leaflet.draw.css";
import "leaflet-draw/dist/images/spritesheet.svg";
import "leaflet-draw/dist/images/marker-shadow.png"
import "leaflet-draw/dist/images/layers-2x.png";
import "leaflet-draw/dist/images/marker-icon-2x.png";
import "leaflet-draw/dist/images/spritesheet.png";
import "leaflet-draw/dist/images/spritesheet-2x.png";
import "leaflet-draw/dist/images/marker-icon.png";
import "leaflet-draw/dist/images/layers.png";

console.log(L.Control.Draw);
L.DrawingLayer = L.FeatureGroup.extend({
  onRemove: function(map) {
	  map.removeControl(this.drawControl);
	  this.clearLayers();
  },
  onAdd: function(map) {
    const drawPluginOptions = {
      position: 'topright',
      draw: {
        polygon: {
          allowIntersection: false, // Restricts shapes to simple polygons
          drawError: {
            color: '#e1e100', // Color the shape will turn when intersects
            message:
              '<strong>Polygon draw does not allow intersections!<strong> (allowIntersection: false)', // Message that will show when intersect
          },
          shapeOptions: {
            color: '#bada55',
          },
        },
	      polyline: false,
	      circlemarker: false,
	      marker: false,
        rectangle: {
          shapeOptions: {
            clickable: false,
          },
        },
      },
      edit: {
        featureGroup: this, // REQUIRED!!
        remove: true,
      },
    };

    // Initialise the draw control and pass it the FeatureGroup of editable layers
    this.drawControl = new L.Control.Draw(drawPluginOptions);
    map.addControl(this.drawControl);
    map.on(L.Draw.Event.CREATED, L.Util.bind(this.drawCreated, this));
  },
  drawCreated: function(e) {
    const type = e.layerType;
    const layer = e.layer;

    if (type === 'marker') {
      layer.bindPopup('A popup!');
    }

    this.addLayer(layer);
  },
});
