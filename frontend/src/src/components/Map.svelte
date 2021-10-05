<script>
  import {onMount} from 'svelte';
  // Import CSS from Leaflet and plugins.
  import 'leaflet/dist/leaflet.css';
  import 'leaflet.markercluster/dist/MarkerCluster.css';
  import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
  import '../leaflet_components/L.TileLayer.QueryableLayer.css';

  // Import JS from Leaflet and plugins.
  import 'leaflet/dist/leaflet';
  import 'leaflet.markercluster/dist/leaflet.markercluster';
  import 'leaflet.gridlayer.googlemutant/Leaflet.GoogleMutant';
  import 'leaflet-search/dist/leaflet-search.src.js';
  import 'leaflet-search/dist/leaflet-search.src.css';
  import '../leaflet_components/L.TileLayer.NutsLayer.js';
  import '../leaflet_components/L.DrawingLayer.js';

  import AreaSelection from './AreaSelection.svelte';
  import DatasetSelection from './DatasetSelection.svelte';
  import CMToggle from './CMToggle.svelte';
  import TopNav from './TopNav.svelte';
  import {selectionStore} from '../stores.js';
  import {INITIAL_MAP_CENTER, INITIAL_ZOOM, BASE_LAYER_URL, BASE_LAYER_PARAMS} from '../settings.js';
  import {WMS_URL} from '../client.js';


  let map;
  // let activeOverlayLayers;
  // let activeCMOutputLayers;

  let selection = null;
  const selectionLayers = {};

  const cmOutputsGroup = L.layerGroup();
  const overlaysGroup = L.layerGroup();
  const selectionsGroup = L.layerGroup();
  const baseLayersGroup = L.layerGroup();


  onMount(async () => {
    console.log('Initialisation of the map');

    // To add the draw toolbar set the option drawControl: true in the map options.
    map = L.map('map', {zoomControl: false});
    map.setView(INITIAL_MAP_CENTER, INITIAL_ZOOM);

    map.addLayer(baseLayersGroup);
    map.addLayer(selectionsGroup);
    map.addLayer(overlaysGroup);
    map.addLayer(cmOutputsGroup);

    const baseLayer = L.tileLayer(BASE_LAYER_URL, BASE_LAYER_PARAMS);
    baseLayersGroup.addLayer(baseLayer); // Add the openstreetmap layer

    // Add the map controls
    map.addControl(makeSearchControl()); // Search tools
    map.addControl(makeCMToggleControl()); // Button to open calculation module pane
    map.addControl(makeAreaSelectionControl());
    map.addControl(makeDatasetSelectionControl());
  });

  function resizeMap() {
    if (map) {
      map.invalidateSize();
    }
  }

  $: {
    // activeSelectionLayer = $activeSelectionLayerStore;
    // activeOverlayLayers = $activeOverlayLayersStore;
    // activeCMOutputLayers = $activeCMOutputLayersStore;
    //
    // syncSelectionLayer();
    // syncOverlayLayers();
    // syncCMOutputLayers();

    updateSelectionLayer($selectionStore);
  }

  // function syncOverlayLayers() {
  //   const overlayToBePruned = new Set(overlaysGroup.getLayers());
  //   for (const activeOverlayLayer of activeOverlayLayers) {
  //     if (!overlaysGroup.hasLayer(activeOverlayLayer)) {
  //       console.log('[Map] Add overlay layer: ' + activeOverlayLayer.name);
  //       overlaysGroup.addLayer(activeOverlayLayer);
  //     } else {
  //       overlayToBePruned.delete(activeOverlayLayer);
  //     }
  //   }
  //   for (const overlay of overlayToBePruned) {
  //     console.log('[Map] Remove overlay layer: ' + overlay.name);
  //     overlaysGroup.removeLayer(overlay);
  //   }
  // }

  function updateSelectionLayer(desiredSelection) {
    if (selection === desiredSelection) {
      return;
    }

    selection = desiredSelection;

    if (desiredSelection == null) {
      selectionsGroup.clearLayers();
      return;
    }

    // Create the layer if necessary
    if (!(desiredSelection in selectionLayers)) {
      if (desiredSelection == 'selection') {
        selectionLayers[desiredSelection] = new L.DrawingLayer();
      } else {
        const layer = L.tileLayer.nutsLayer(
            WMS_URL,
            {
              transparent: 'true',
              layers: desiredSelection + '.geojson',
              format: 'image/png',
            },
        );

        layer.setZIndex(1000);

        selectionLayers[desiredSelection] = layer;
      }
    }

    const layer = selectionLayers[desiredSelection];

    if (!selectionsGroup.hasLayer(layer)) {
      selectionsGroup.clearLayers();
      selectionsGroup.addLayer(layer);
    }
  }

  // function syncCMOutputLayers() {
  //   const cmOutputsToBePruned = new Set(cmOutputsGroup.getLayers());
  //   for (const activeCMOutputLayer of activeCMOutputLayers) {
  //     if (!cmOutputsGroup.hasLayer(activeCMOutputLayer)) {
  //       console.log('[Map] Add CM output layer: ' + activeCMOutputLayer.id);
  //       cmOutputsGroup.addLayer(activeCMOutputLayer);
  //     } else {
  //       cmOutputsToBePruned.delete(activeCMOutputLayer);
  //     }
  //   }
  //   for (const cmOutput of cmOutputsToBePruned) {
  //     console.log('[Map] Remove CM output layer: ' + cmOutput.id);
  //     cmOutputsGroup.removeLayer(cmOutput);
  //   }
  // }

  /* Left control (area selection and overlay layers)*/
  function makeAreaSelectionControl() {
    const ctr = L.control({position: 'topleft'});
    ctr.onAdd = (map) => {
      const overlayDiv = L.DomUtil.create('div' );
      L.DomUtil.addClass(overlayDiv, 'testComponent');
      toolbar = new AreaSelection({target: overlayDiv});
      return overlayDiv;
    };
    return ctr;
  }

  /* Left control (area selection and overlay layers)*/
  function makeDatasetSelectionControl() {
    const ctr = L.control({position: 'topleft'});
    ctr.onAdd = (map) => {
      const areaDiv = L.DomUtil.create('div' );
      L.DomUtil.addClass(areaDiv, 'testComponent');
      toolbar = new DatasetSelection({target: areaDiv});
      return areaDiv;
    };
    return ctr;
  }

  /* Left control (area selection and overlay layers)*/
  // function makeOverlayLayersControl() {
  //   const ctr = L.control({position: 'topleft'});
  //   ctr.onAdd = (map) => {
  //     const areaDiv = L.DomUtil.create('div' );
  //     L.DomUtil.addClass(areaDiv, 'testComponent');
  //     toolbar = new LayerSelection({target: areaDiv});
  //     return areaDiv;
  //   };
  //   return ctr;
  // }

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

  function makeSearchControl() {
    const searchControl = new L.Control.Search({
      container: 'findbox',
      url: 'https://nominatim.openstreetmap.org/search?format=json&q={s}',
      jsonpParam: 'json_callback',
      propertyName: 'display_name',
      textPlaceholder: 'Search place...',
      propertyLoc: ['lat', 'lon'],
      marker: false, // L.circleMarker([0, 0], { radius: 30 }),
      autoCollapse: false,
      autoType: false,
      minLength: 2,
      collapsed: false,
      autoResize: false,
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
    border: 0px;
  }
</style>


<svelte:window on:resize={resizeMap} />

<div id="page">
  <TopNav><div id="findbox"> </div></TopNav>
  <div id="map"></div>
</div>
