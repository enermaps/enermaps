import {popupInformation, popupInformationtitle, isCMPaneActiveStore} from '../stores.js';


export const popupContent = '';
export const popupContenttitle = '';


const BaseMethods = {
  onError: function(err) {
    console.log(err);
  },

  getFeatureInfo: async function(point) {
    const url = this._getFeatureInfoUrl(point);

    return fetch(url)
        .then((response) => {
          if (response.ok) {
            return response.json().catch((error) => {
              console.error('Error:', error);
              return null;
            }).then((data) => {
              return data;
            });
          } else {
            console.error('Failed to retrieve the features');
            return null;
          }
        })
        .catch((error) => {
          console.error('Error:', error.message);
          return null;
        });
  },

  showInfos: function(title, latlng, content) {
    // Otherwise show the content in a popup, or something.
    if (!content || !content.features || (content.features.length == 0)) {
      return false;
    }

    let popupContent = '';
    let popupContenttitle = '';
    const allFields = {};

    // popupContenttitle += '<h1>' + title + '</h1>';
    popupContenttitle += title;


    for (const feature of content.features) {
      const properties = feature.properties;

      const variables = JSON.parse(properties.variables);
      const units = JSON.parse(properties.units);

      const variableNames = Object.keys(variables).sort();

      for (const key of variableNames) {
        const value = variables[key];

        if (value !== null) {
          popupContent += '<tr id="hdata">';

          const td1 = document.createElement('td');
          td1.className = 'name';
          td1.innerText = key + ' :';
          popupContent += td1.outerHTML;

          const td2 = document.createElement('td');
          td2.className = 'value';
          td2.innerText = value;

          if (key in units) {
            const unit = units[key];
            if ((unit !== undefined) && (unit !== null) && (unit !== '-')) {
              td2.innerText += ' ' + unit;
            }
          }
          popupContent += td2.outerHTML;
          popupContent += '</tr>';
        }
      }

      if (properties.fields !== undefined) {
        const fields = JSON.parse(properties.fields);

        for (const [key, value] of Object.entries(fields)) {
          if (allFields[key] === undefined) {
            allFields[key] = value;
          }
        }
      }
    }

    const fieldNames = Object.keys(allFields).sort();

    for (const key of fieldNames) {
      const value = allFields[key];

      if ((value !== null) && (key == 'Demande')) {
        popupContent += '<tr id="pdata">';

        const td1 = document.createElement('td');
        td1.className = 'name';
        td1.innerText = key + ' :';
        popupContent += td1.outerHTML;

        const td2 = document.createElement('td');
        td2.className = 'value';
        td2.innerText = value;
        popupContent += td2.outerHTML;

        popupContent += '</tr>';
      }
    }

    if (popupContent.length != 0) {
      L.popup({
        minWidth: 400,
        maxWidth: 800,
        minHeight: 300,
        maxHeight: 500,
        className: 'wms_feature_info',
      })
          .setLatLng(latlng)
          .setContent('<table><tbody>' + popupContent + '</tbody></<table>')
          .openOn(this._map);
      popupInformation.set(popupContent);
      popupInformationtitle.set(popupContenttitle);
      console.log(popupContent);
      isCMPaneActiveStore.set(true);
    }
    popupInformation.set(popupContent);
    popupInformationtitle.set(popupContenttitle);
    isCMPaneActiveStore.set(true);
    return true;
  },

  highlightArea: function(data) {
    const geometryType = data.features[0].geometry.type;

    if ((geometryType == 'MultiPolygon') || (geometryType == 'Polygon')) {
      this.selection = L.geoJSON(
          null,
          {
            style: {
              color: '#FF7800',
              weight: 2,
              opacity: 1,
            },
          },
      );

      this.selection.setZIndex(this.zIndex + 1);

      this.selection.addTo(this._map);

      for (const feature of data.features) {
        this.selection.addData(feature);
      }
    }
  },

  resetHighlightedArea: function() {
    if (this.selection != null) {
      this._map.removeLayer(this.selection);
    }

    this._map.closePopup();
    this.selection = null;
  },

  _getFeatureInfoUrl: function(point) {
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

    const url = (this._wmsUrl !== undefined ? this._wmsUrl : this._url);

    return url + L.Util.getParamString(params, url, true);
  },

  _convertField: function(value) {
    // Fields containing JSON data (in string format) might be truncated (due to some
    // file format limitation), and thus not be valid JSON. We try to extract as many
    // info as possible from it anyway by building a valid JSON string.
    let jsonValue = null;

    if (!value.endsWith('}')) {
      value += '}';
    }

    try {
      jsonValue = JSON.parse(value);
    } catch {
      let index = value.lastIndexOf(',');
      while ((jsonValue === null) && (index > 0)) {
        value = value.substring(0, index) + '}';

        try {
          jsonValue = JSON.parse(value);
        } catch {
          index = value.lastIndexOf(',');
        }
      }
    }

    if (jsonValue !== null) {
      return jsonValue;
    } else {
      return {};
    }
  },
};


L.TileLayer.QueryableLayer = L.TileLayer.WMS.extend(BaseMethods).extend({
});


L.NonTiledLayer.QueryableLayer = L.NonTiledLayer.WMS.extend(BaseMethods).extend({
});


L.tileLayer.queryableLayer= function(url, options) {
  return new L.TileLayer.QueryableLayer(url, options);
};


L.nonTiledLayer.queryableLayer= function(url, options) {
  return new L.NonTiledLayer.QueryableLayer(url, options);
};
