L.DrawingLayer = L.FeatureGroup.extend({
  onRemove: function(map) {
	  map.removeControl(this.drawControl);
	  this.clearLayers();
	    $('#indicator').prop('disabled', true);
	    $('#indicator').off();
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
    $('#indicator').prop('disabled', false);
    $('#indicator').click(L.Util.bind(this.onIndicatorClick, this));
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
