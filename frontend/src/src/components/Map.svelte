<script>
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

import LayerSelection from './LayerSelection.svelte';
import { activeOverlayLayersStore, activeSelectionLayerStore } from '../stores.js'

import {INITIAL_MAP_CENTER, INITIAL_ZOOM} from '../settings.js';

let map;
$: activeSelectionLayer = $activeSelectionLayerStore;
$: activeOverlayLayers = $activeOverlayLayersStore;

const overlaysGroup = L.layerGroup();
const selectionsGroup = L.layerGroup();
const baseLayersGroup = L.layerGroup();


onMount(async () => {
  console.log('init map');
  map = L.map('map').setView(INITIAL_MAP_CENTER, INITIAL_ZOOM);


  map.addLayer(baseLayersGroup);
  map.addLayer(selectionsGroup);
  map.addLayer(overlaysGroup);

  const baseLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy;' +
' <a href="https://cartodb.com/attributions">CartoDB</a>'});
  baseLayersGroup.addLayer(baseLayer);

  map.addControl(makeSearchControl());
  map.addControl(makeLayerControl());
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
function makeLayerControl() {
  let layerControl = L.control({ position: "topright" });
  layerControl.onAdd = (map) => {
    let div = L.DomUtil.create("div");
    L.DomUtil.addClass(div, "leaflet-control-layers");
    toolbar = new LayerSelection({ target: div});
    return div;
  };
  return layerControl;
}
function makeSearchControl() {
  const searchControl = new L.Control.Search({
    url: 'https://nominatim.openstreetmap.org/search?format=json&q={s}',
    jsonpParam: 'json_callback',
    propertyName: 'display_name',
    propertyLoc: ['lat', 'lon'],
    marker: false, // L.circleMarker([0, 0], { radius: 30 }),
    autoCollapse: true,
    autoType: false,
    minLength: 2,
  });
  return searchControl;
}
</script>
<style>
#map {
  width: 100%;
  height: 100%;
}
</style>

<svelte:window on:resize={resizeMap} />

<div id="map"></div>
