L.TileLayer.QueryableLayer = L.TileLayer.WMS.extend({
  onAdd: function(map) {
    // Triggered when the layer is added to a map.
    //  Register a click listener, then do all the upstream WMS things
    L.TileLayer.WMS.prototype.onAdd.call(this, map);
    map.on('click', this.getFeatureInfo, this);
  },

  onRemove: function(map) {
    // Triggered when the layer is removed from a map.
    //   Unregister a click listener, then do all the upstream WMS things
    L.TileLayer.WMS.prototype.onRemove.call(this, map);
    map.off('click', this.getFeatureInfo, this);
  },
  getFeatureInfo: function(evt) {
    const point = this._map.latLngToContainerPoint(evt.latlng,
        this._map.getZoom());

    const url = this.getFeatureInfoUrl(point);
    const showResults = L.Util.bind(this.showResults, this);
    fetch(url).then((response) => response.json()).catch((error) => {
      console.error('Error:', error);
    }).then((data) => {
      showResults(evt.latlng, data);
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
  onError: function(err) {
    console.log(err);
  },
  showResults: function(latlng, content) {
    // Otherwise show the content in a popup, or something.
    if (!content || !content.features) {
      return;
    }
    let popupContent = "";
    for (const feature of content.features) {
      const properties = feature.properties;
      //iterate over all feature and make them into k-v
      for (const [key, value] of Object.entries(properties)) {
        const dt = document.createElement('dt');
        dt.innerText = key;
        popupContent += dt.outerHTML;
        const dd = document.createElement('dd');
        dd.innerText = value;
        popupContent += dd.outerHTML;
      }
    }
    if (popupContent.length != 0) {
      console.log(content);
      let popup = L.popup({maxwidth: 500, maxHeight: 200})
        .setLatLng(latlng)
        .setContent(popupContent)
        .openOn(this._map);
      //popup.maxHeight = 100;
      }
    },
});

L.tileLayer.queryableLayer= function(url, options) {
  return new L.TileLayer.QueryableLayer(url, options);
};
