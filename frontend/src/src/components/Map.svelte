<script >
import {onMount} from 'svelte';

// Import CSS from Leaflet and plugins.
import 'leaflet/dist/leaflet.css';
//import 'frontend/leaflet/';
//import '../../public/leaflet/leaflet.css';
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
import TopNav from './TopNav.svelte';

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
  // To add the draw toolbar set the option drawControl: true in the map options.
  map = L.map('map', {zoomControl : false})
  map.setView(INITIAL_MAP_CENTER, INITIAL_ZOOM);

  map.addLayer(baseLayersGroup);  
  map.addLayer(selectionsGroup);  
  map.addLayer(overlaysGroup);   

  const baseLayer = L.tileLayer(BASE_LAYER_URL, BASE_LAYER_PARAMS);
  baseLayersGroup.addLayer(baseLayer); // Add the openstreetmap layer

  // Add the map controls
  map.addControl(makeSearchControl())   // Search tools
  map.addControl(makeCMToggleControl());  // Button to open calculation module pane
  //map.addControl(makeLeftControls());   // Area selection and overlay layers
  map.addControl(makeAreaSelectionControl());
  map.addControl(makeOverlayLayersControl());
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


/* Left control (area selection and overlay layers)*/
function makeAreaSelectionControl() {
  const ctr = L.control({position: 'topleft'});
  ctr.onAdd = (map) => {
    const overlay_div = L.DomUtil.create('div', );
    L.DomUtil.addClass(overlay_div, 'testComponent');
    toolbar = new LayerSelection({target: overlay_div});
    return overlay_div;
  };  
  return ctr;
}

/* Left control (area selection and overlay layers)*/
function makeOverlayLayersControl() {
  const ctr = L.control({position: 'topleft'});
  ctr.onAdd = (map) => {
    const area_div = L.DomUtil.create('div', );
    L.DomUtil.addClass(area_div, 'testComponent');
    toolbar = new AreaSelection({target: area_div})
    // Enable the overlay layers to be dragged
    // var draggable = new L.Draggable(area_div);
    // draggable.enable();
    return area_div;
  };
  return ctr;
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
    container : 'findbox',
    url: 'https://nominatim.openstreetmap.org/search?format=json&q={s}',
    jsonpParam: 'json_callback',
    propertyName: 'display_name',
    propertyLoc: ['lat', 'lon'],
    marker: false, // L.circleMarker([0, 0], { radius: 30 }),
    autoCollapse: false,
    autoResize: false,
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

#page {
  width: 100%;
  height: 100%;
  display: flex;
  box-sizing: border-box;
  flex-direction: column;
}

#map {
  width: 100%;
  height: 100%;
  display: flex;
  box-sizing: border-box;
}

#findbox {
  display: inline-block;
  overflow: visible;
  vertical-align: middle;
  margin-left: 35px;
}

</style>

<svelte:window on:resize={resizeMap} />

<div id="page">
  <TopNav><div id="findbox"> </div></TopNav>
  <div id="map"></div>
</div>