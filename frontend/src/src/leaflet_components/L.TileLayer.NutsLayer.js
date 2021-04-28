/*
A Web Map Service (WMS) is a standard protocol developed by the Open Geospatial
Consortium in 1999 for serving georeferenced map images over the Internet.[1]
These images are typically produced by a map server from data provided by
a GIS database.
*/

L.TileLayer.NutsLayer = L.TileLayer.WMS.extend({
  onAdd: function(map) {
    this.selection = L.geoJSON();
    const myStyle = {
      color: '#ff7800',
      weight: 10,
      opacity: 1,
    };
    this.selection.style = myStyle;
    this.selection.addTo(this._map);
    // Triggered when the layer is added to a map.
    //   Register a click listener, then do all the upstream WMS things
    L.TileLayer.WMS.prototype.onAdd.call(this, map);
    map.on('click', this.getFeatureInfo, this);
  },

  onRemove: function(map) {
    // Triggered when the layer is removed from a map.
    //   Unregister a click listener, then do all the upstream WMS things
    L.TileLayer.WMS.prototype.onRemove.call(this, map);
    map.off('click', this.getFeatureInfo, this);
    this._map.removeLayer(this.selection);
    this.selection = undefined;
  },
  getSelection: function() {
    return this.selection.toGeoJSON();
  },
  getFeatureInfo: function(evt) {
    const point = this._map.latLngToContainerPoint(evt.latlng,
        this._map.getZoom());

    const url = this.getFeatureInfoUrl(point);
    const showResults = L.Util.bind(this.onClickSelect, this);
    fetch(url).then((response) => response.json()).catch((error) => {
      console.error('Error:', error);
    }).then((data) => {
      showResults(undefined, data);
    });
  },

  getFeatureInfoUrl: function(point) {
    // Construct a GetFeatureInfo request URL given a point
    // TODO this one is way trickier than it seems for WMS 1.1.1 vs 1.3.0,
    // currently the backend and the frontend understand that:
    // * the bounding box in the map coordinate
    // * the X and Y position are pixels offset
    // This behaviour changes between WMS version, so verify that the backend is
    // talking version 1.1.1 of the WMS
    const size = this._map.getSize();
    const crs = this._map.options.crs;
    const mapBounds = this._map.getBounds();
    const nw = crs.project(mapBounds.getNorthWest());
    const se = crs.project(mapBounds.getSouthEast());
    const params = {
      request: 'GetFeatureInfo',
      service: 'WMS',
      srs: crs.code,
      styles: this.wmsParams.styles,
      transparent: this.wmsParams.transparent,
      version: this.wmsParams.version,
      format: this.wmsParams.format,
      bbox: nw.x + ',' + se.y + ',' + se.x + ',' + nw.y,
      height: size.y,
      width: size.x,
      layers: this.wmsParams.layers,
      query_layers: this.wmsParams.layers,
      info_format: 'application/json',
    };
    if (!!this.wmsParams.cql_filter) {
      params.cql_filter = this.wmsParams.cql_filter;
    }

    params[params.version === '1.3.0' ? 'i' : 'x'] = Math.floor(point.x);
    params[params.version === '1.3.0' ? 'j' : 'y'] = Math.floor(point.y);

    return this._url + L.Util.getParamString(params, this._url, true);
  },
  getFeatureId: function(feature) {
    if (!!feature.properties.nuts_id) {
      return feature.properties.nuts_id;
    }
    return feature.id;
  },
  onError: function(err) {
    console.log(err);
  },
  onClickSelect: function(err, content) {
    // if (err) { console.log(err); return; } // do nothing if there's an error
    // Otherwise show the content in a popup, or something.
    // this._map.getLayer("selection")
    // check if we already clicked to toggle the selection
    console.log('check click');
    // this._map.removeLayer(this.selection);
    // to be replaced by a dict to find the data per id
    for (const feature of content.features) {
      const newFeatureId = this.getFeatureId(feature);
      let layerRemoved = false;
      this.selection.eachLayer((layer) => {
        const featureId = this.getFeatureId(layer.feature);
        if (newFeatureId == featureId) {
          this.selection.removeLayer(layer);
          layerRemoved = true;
        }
      });
      if (!layerRemoved) {
        this.selection.addData(feature);
      }
    }
    console.log(this.selection.toGeoJSON().features.map(this.getFeatureId));
  },
});

L.tileLayer.nutsLayer = function(url, options) {
  return new L.TileLayer.NutsLayer(url, options);
};
