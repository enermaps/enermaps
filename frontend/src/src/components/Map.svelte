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
  import '../leaflet_components/L.TileLayer.QueryableLayer.js';
  import '../leaflet_components/L.DrawingLayer.js';

  import LeftPanel from './LeftPanel.svelte';
  import CMToggle from './CMToggle.svelte';
  import CMList from './CMList.svelte';
  import TopNav from './TopNav.svelte';

  import {areaSelectionStore, layersStore, areaSelectionLayerStore} from '../stores.js';
  import {INITIAL_MAP_CENTER, INITIAL_ZOOM, BASE_LAYER_URL, BASE_LAYER_PARAMS} from '../settings.js';
  import {WMS_URL} from '../client.js';
  import {recomputeLayer} from '../layers.js';


  let map;

  let selection = null;
  const selectionLayers = {};

  const cmOutputsGroup = L.layerGroup();
  const overlaysGroup = L.layerGroup();
  const selectionsGroup = L.layerGroup();
  const baseLayersGroup = L.layerGroup();

  let leftPanel = null;


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
    map.addControl(makeCMListControl());
    map.addControl(makeLeftPanel());
  });


  function resizeMap() {
    if (map) {
      map.invalidateSize();
    }
  }


  $: {
    updateSelectionLayer($areaSelectionStore);
    updateOverlayLayers($layersStore);
  }


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
        selectionLayers[desiredSelection].panel = leftPanel;
      } else {
        const layer = L.tileLayer.nutsLayer(
            WMS_URL,
            {
              transparent: 'true',
              layers: 'area/' + desiredSelection,
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

    $areaSelectionLayerStore = layer;
  }


  function updateOverlayLayers(layers) {
    const layersToBePruned = new Set(overlaysGroup.getLayers());

    for (let i = 0; i < layers.length; ++i) {
      const layer = layers[i];

      if (layer.leaflet_layer !== null) {
        layersToBePruned.delete(layer.leaflet_layer);
      }

      if (layer.visible && (layer.effect !== 'compute')) {
        if (layer.leaflet_layer === null) {
          if (layer.is_raster) {
            layer.leaflet_layer = L.tileLayer.wms(
                WMS_URL,
                {
                  transparent: 'true',
                  layers: encodeURIComponent(layer.name),
                  format: 'image/png',
                },
            );
          } else {
            layer.leaflet_layer = L.tileLayer.queryableLayer(
                WMS_URL,
                {
                  transparent: 'true',
                  layers: encodeURIComponent(layer.name),
                  format: 'image/png',
                },
            );
          }

          if (layer.task_id !== null) {
            layer.leaflet_layer.on(
                'tileerror',
                () => {
                  recomputeLayer(layer, overlaysGroup);
                },
            );
          }
        }

        layer.leaflet_layer.setZIndex(layers.length - i);

        if (!overlaysGroup.hasLayer(layer.leaflet_layer)) {
          console.log('[Map] Add overlay layer: ' + layer.name);
          overlaysGroup.addLayer(layer.leaflet_layer);
        }
      } else if (layer.leaflet_layer !== null) {
        if (overlaysGroup.hasLayer(layer.leaflet_layer)) {
          console.log('[Map] Remove overlay layer: ' + layer.name);
          overlaysGroup.removeLayer(layer.leaflet_layer);
        }
      }
    }

    for (const leafletLayer of layersToBePruned) {
      overlaysGroup.removeLayer(leafletLayer);
    }
  }


  function makeLeftPanel() {
    const ctr = L.control({position: 'topleft'});

    ctr.onAdd = (map) => {
      const container = L.DomUtil.create('div' );
      leftPanel = new LeftPanel({target: container});
      leftPanel.disableMapScrolling(map);
      return container;
    };

    return ctr;
  }


  function makeCMToggleControl() {
    const CMToggleControl = L.control({position: 'topright'});
    CMToggleControl.onAdd = (map) => {
      const div = L.DomUtil.create('div');
      toolbar = new CMToggle({target: div});
      return div;
    };
    return CMToggleControl;
  }


  function makeCMListControl() {
    const CMToggleControl = L.control({position: 'topright'});
    CMToggleControl.onAdd = (map) => {
      const div = L.DomUtil.create('div');
      toolbar = new CMList({target: div});
      disableMapScrolling(div);
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


  function disableMapScrolling(element) {
    // Disable dragging when user's cursor enters the element
    element.addEventListener('mouseover', function() {
      map.dragging.disable();
    });

    // Re-enable dragging when user's cursor leaves the element
    element.addEventListener('mouseout', function() {
      map.dragging.enable();
    });
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
