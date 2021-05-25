import 'leaflet-draw/dist/leaflet.draw.js';
import 'leaflet-draw/dist/leaflet.draw.css';

L.DrawingLayer = L.FeatureGroup.extend({
  onRemove: function(map) {
    map.removeControl(this.drawControl);
    this.clearLayers();
  },
  onAdd: function(map) {
    const drawPluginOptions = {
      position: 'topleft',
      draw: {
        polygon: {
          allowIntersection: true,
          shapeOptions: {
            color: '#4d88c7',
          },
        },
        polyline: false,
        circlemarker: false,
        marker: false,
        rectangle: false,
        circle: false,
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

  getSelection: function() {
    return this.toGeoJSON();
  },

  drawCreated: function(e) {
    const layer = e.layer;
    this.addLayer(layer);
  },
});
