<script >
import {onMount} from 'svelte';

// Import CSS from Leaflet and plugins.
import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';

// Import images directly that got missed via the CSS imports above.
// import 'leaflet/dist/images/marker-icon-2x.png';
// import 'leaflet/dist/images/marker-shadow.png';

// Import JS from Leaflet and plugins.
import 'leaflet/dist/leaflet';
import 'leaflet.markercluster/dist/leaflet.markercluster';
import 'leaflet.gridlayer.googlemutant/Leaflet.GoogleMutant';
import 'leaflet-search/dist/leaflet-search.src.js';
import 'leaflet-search/dist/leaflet-search.src.css';

import AreaSelection from './AreaSelection.svelte';
import LayerSelection from './LayerSelection.svelte';
import CMToggle from './CMToggle.svelte';

import {activeOverlayLayersStore, activeSelectionLayerStore} from '../stores.js';

import {INITIAL_MAP_CENTER, INITIAL_ZOOM, BASE_LAYER_URL} from '../settings.js';
import {BASE_LAYER_PARAMS} from '../settings.js';

let map;

$: activeSelectionLayer = $activeSelectionLayerStore;
$: activeOverlayLayers = $activeOverlayLayersStore;

const overlaysGroup = L.layerGroup();  // energy map etc
const selectionsGroup = L.layerGroup();  // nuts and custom selection layer
const baseLayersGroup = L.layerGroup();  // openstreetmap ?


onMount(async () => {
  console.log('init map');
  map = L.map('map', {zoomControl : false})
  map.setView(INITIAL_MAP_CENTER, INITIAL_ZOOM);

  map.addLayer(baseLayersGroup);  
  map.addLayer(selectionsGroup);  
  map.addLayer(overlaysGroup);   

  const baseLayer = L.tileLayer(BASE_LAYER_URL, BASE_LAYER_PARAMS);
  baseLayersGroup.addLayer(baseLayer); // Add the openstreetmap layer

  // Add the "left" tools
  map.addControl(makeSearchControl())   // Search tools
  map.addControl(makeLayerControl());   // Box with the area selection layers 
  map.addControl(makeAreaSelectionControl())  // Separate box with only the overlay layers
  map.addControl(makeCMToggleControl());  // Button to open calculation module pane
});

function resizeMap() {
  if (map) {
    map.invalidateSize();
  }
}

$: {
  console.log(`selected layer was changed: ${activeSelectionLayer}`);
  console.log(`overlay layer was changed: ${activeOverlayLayers}`);
  syncSelectionLayer();
  syncOverlayLayers();
}

function syncOverlayLayers() {
  const overlayToBePruned = new Set(overlaysGroup.getLayers());
  for (const activeOverlayLayer of activeOverlayLayers) {
    if (!overlaysGroup.hasLayer(activeOverlayLayer)) {
      overlaysGroup.addLayer(activeOverlayLayer);
    } else {
      overlayToBePruned.delete(activeOverlayLayer);
    }
  }
  for (const overlay of overlayToBePruned) {
    overlaysGroup.removeLayer(overlay);
  }
}

function syncSelectionLayer() {
  if (!activeSelectionLayer) {
    return;
  }
  if (!selectionsGroup.hasLayer(activeSelectionLayer)) {
    // currently the activated layer is not the right one
    // so remove it
    selectionsGroup.clearLayers();
  }
  if (selectionsGroup.getLayers().length === 0) {
    selectionsGroup.addLayer(activeSelectionLayer);
  }
}

/* Box for the */
function makeLayerControl() {
  const layerControl = L.control({position: 'topleft'});
  layerControl.onAdd = (map) => {
    const div = L.DomUtil.create('div');
    L.DomUtil.addClass(div, 'test');
    toolbar = new LayerSelection({target: div});
    return div;
  };
  return layerControl;
}

/* Box for */
function makeAreaSelectionControl() {
  const areaSelectionControl = L.control({position: 'topright'});
  areaSelectionControl.onAdd = (map) => {
    const div = L.DomUtil.create('div');
    L.DomUtil.addClass(div, 'test');
    toolbar = new AreaSelection({target: div})
    return div
  };
  return areaSelectionControl;
}


function makeCMToggleControl() {
  const CMToggleControl = L.control({position: 'topright'});
  CMToggleControl.onAdd = (map) => {
    const div = L.DomUtil.create('div');
    L.DomUtil.addClass(div, 'test');
    toolbar = new CMToggle({target: div});
    return div;
  };
  return CMToggleControl;
}

// https://github.com/stefanocudini/leaflet-search
function makeSearchControl() {
  const searchControl = new L.Control.Search({
    position : 'topleft',
    url: 'https://nominatim.openstreetmap.org/search?format=json&q={s}',
    jsonpParam: 'json_callback',
    propertyName: 'display_name',
    propertyLoc: ['lat', 'lon'],
    marker: false, // L.circleMarker([0, 0], { radius: 30 }),
    autoCollapse: false,
    autoType: false,
    minLength: 2,
    collapsed: false,
    textPlaceholder: 'Search location...',
    moveToLocation: function(latlng, title, map) {
  			map.setView(latlng, 12); // access the zoom
		}
  });

  return searchControl;
}

</script>

<style>

#map {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}

</style>

<svelte:window on:resize={resizeMap} />

<div id="map"></div>
