L.TileLayer.NutsLayer = L.TileLayer.WMS.extend({
  onAdd: function (map) {
    // Triggered when the layer is added to a map.
    //   Register a click listener, then do all the upstream WMS things
    L.TileLayer.WMS.prototype.onAdd.call(this, map);
    map.on("click", this.getFeatureInfo, this);
    $("#indicator").prop("disabled", false);
    $("#indicator").click(L.Util.bind(this.onIndicatorClick, this));
  },

  onRemove: function (map) {
    // Triggered when the layer is removed from a map.
    //   Unregister a click listener, then do all the upstream WMS things
    L.TileLayer.WMS.prototype.onRemove.call(this, map);
    map.off("click", this.getFeatureInfo, this);
    if (!!this.selection) {
      this._map.removeLayer(this.selection);
      this.selection = undefined;
    }
    $("#indicator").prop("disabled", true);
    $("#indicator").off();
  },
  onIndicatorClick: function (evt) {
    if (!!!this.selection) {
      //no selection yet
      return;
    }
    var selected_overlay = [];
    console.log(
      this._map.eachLayer((layer) => {
        if (!!layer.is_overlay) {
          selected_overlay.push(layer.wmsParams.layers);
        }
      })
    );
    if (selected_overlay.length == 0) {
      //endpoint for the calculation module
      return;
    }
	  $.ajax({
		url: "http://127.0.0.1:5000/raster"
	  })
    console.log(
      this.selection.toGeoJSON().features.map(this.getFeatureId),
      selected_overlay
    );
  },
  getFeatureInfo: function (evt) {
    // Make an AJAX request to the server and hope for the best
    var url = this.getFeatureInfoUrl(evt.latlng),
      showResults = L.Util.bind(this.onClickSelect, this);
    $.ajax({
      url: url,
      success: function (data, status, xhr) {
        var err = typeof data === "string" ? null : data;
        showResults(err, evt.latlng, data);
      },
      error: function (xhr, status, error) {
        showResults(error);
      },
    });
  },

  getFeatureInfoUrl: function (latlng) {
    // Construct a GetFeatureInfo request URL given a point
    var point = this._map.latLngToContainerPoint(latlng, this._map.getZoom()),
      size = this._map.getSize(),
      params = {
        request: "GetFeatureInfo",
        service: "WMS",
        srs: this.wmsParams.srs,//"EPSG:4326",
        styles: this.wmsParams.styles,
        transparent: this.wmsParams.transparent,
        version: this.wmsParams.version,
        format: this.wmsParams.format,
        bbox: this._map.getBounds().toBBoxString(),
        height: size.y,
        width: size.x,
        layers: this.wmsParams.layers,
        query_layers: this.wmsParams.layers,
        info_format: "application/json",
      };
    if (!!this.wmsParams.cql_filter) {
      params.cql_filter = this.wmsParams.cql_filter;
    }

    params[params.version === "1.3.0" ? "i" : "x"] = point.x;
    params[params.version === "1.3.0" ? "j" : "y"] = point.y;

    return this._url + L.Util.getParamString(params, this._url, true);
  },
  getFeatureId: function (feature) {
    if (!!feature.properties.nuts_id) {
      return feature.properties.nuts_id;
    }
    return feature.id;
  },
  onError: function (err) {
    console.log(err);
  },
  onClickSelect: function (content, latlng, content) {
    //if (err) { console.log(err); return; } // do nothing if there's an error
    // Otherwise show the content in a popup, or something.
    //this._map.getLayer("selection")
    var myStyle = {
      color: "#ff7800",
      weight: 10,
      opacity: 1,
    };
    if (!!!this.selection) {
      this.selection = L.geoJSON();
      this.selection.style = myStyle;
      this.selection.addTo(this._map);
    }
    //check if we already clicked to toggle the selection
    console.log("check click");
    //this._map.removeLayer(this.selection);
    //to be replaced by a dict to find the data per id
    for (const i in content.features) {
      const feature = content.features[i];
      const new_feature_id = this.getFeatureId(feature);
      var layer_removed = false;
      this.selection.eachLayer((layer) => {
        const feature_id = this.getFeatureId(layer.feature);
        if (new_feature_id == feature_id) {
          this.selection.removeLayer(layer);
          layer_removed = true;
        }
      });
      if (!layer_removed) {
        this.selection.addData(feature);
      }
    }
    //this.selection_by_id[content.properties.nuts_id] = content;
    console.log(this.selection.toGeoJSON().features.map(this.getFeatureId));
    //this.selection = L.geoJSON(content, {style: myStyle});
    //this.selection.id = "selection";
  },
});

L.tileLayer.nutsLayer = function (url, options) {
  return new L.TileLayer.NutsLayer(url, options);
};
