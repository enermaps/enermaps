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
  import 'leaflet.nontiledlayer/dist/NonTiledLayer-src.js';
  import '../leaflet_components/L.TileLayer.NutsLayer.js';
  import '../leaflet_components/L.TileLayer.QueryableLayer.js';
  import '../leaflet_components/L.DrawingLayer.js';

  import LeftPanel from './LeftPanel.svelte';
  import CMToggle from './CMToggle.svelte';
  import CMList from './CMList.svelte';
  import TopNav from './TopNav.svelte';

  import {areaSelectionStore, layersStore, areaSelectionLayerStore, isCMPaneActiveStore} from '../stores.js';
  import {INITIAL_MAP_CENTER, INITIAL_ZOOM, BASE_LAYER_URL, BASE_LAYER_PARAMS} from '../settings.js';
  import {WMS_URL} from '../client.js';
  import {recomputeLayer, markLayerAsRefreshing, markLayerAsRefreshed} from '../layers.js';


  let map;

  let selection = null;
  const selectionLayers = {};

  let highlightedLayer = null;

  const cmOutputsGroup = L.layerGroup();
  const overlaysGroup = L.layerGroup();
  const selectionsGroup = L.layerGroup();
  const baseLayersGroup = L.layerGroup();

  let leftPanel = null;

  let minZoomLevel = 0;
  let displayZoomWarning = false;


  onMount(async () => {
    console.log('Initialisation of the map');

    // To add the draw toolbar set the option drawControl: true in the map options.
    map = L.map('map', {zoomControl: false, minZoom: 2});
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

    map.on('zoomend', updateZoomWarning);
    map.on('click', onMapClicked);
  });


  function resizeMap() {
    if (map) {
      map.invalidateSize();
    } else {
      setTimeout(resizeMap, 100);
    }
  }


  $: {
    const isCMPaneActive = $isCMPaneActiveStore;

    if (isCMPaneActive) {
      if (highlightedLayer != null) {
        highlightedLayer.leaflet_layer.resetHighlightedArea();
        highlightedLayer = null;
      }
    }

    updateSelectionLayer($areaSelectionStore);
    updateOverlayLayers($layersStore);
  }


  function updateZoomWarning() {
    if (map) {
      displayZoomWarning = (map.getZoom() < minZoomLevel);
    }
  }


  async function onMapClicked(event) {
    const layers = $layersStore;

    if (highlightedLayer != null) {
      highlightedLayer.leaflet_layer.resetHighlightedArea();
      highlightedLayer = null;
    }

    if ($isCMPaneActiveStore) {
      return;
    }

    const point = map.latLngToContainerPoint(event.latlng, map.getZoom());

    for (let i = 0; i < layers.length; ++i) {
      const layer = layers[i];

      if (layer.visible && (layer.leaflet_layer !== null) &&
          ((layer.leaflet_layer instanceof L.TileLayer.QueryableLayer) ||
           (layer.leaflet_layer instanceof L.NonTiledLayer.QueryableLayer))) {
        const data = await layer.leaflet_layer.getFeatureInfo(point);

        let title;
        if (layer.labels.dataset != null) {
          title = layer.labels.dataset;

          if (layer.labels.secondary != null) {
            title += ' - ' + layer.labels.secondary;
          }
        } else {
          title = layer.labels.primary;
        }

        if (layer.leaflet_layer.showInfos(title, event.latlng, data)) {
          layer.leaflet_layer.highlightArea(data);
          highlightedLayer = layer;
          break;
        }
      }
    }
  }


  function updateSelectionLayer(desiredSelection) {
    if (!$isCMPaneActiveStore) {
      desiredSelection = null;
    }

    if (selection === desiredSelection) {
      return;
    }

    selection = desiredSelection;

    if (desiredSelection == null) {
      selectionsGroup.clearLayers();
      $areaSelectionLayerStore = null;
      return;
    }

    // Create the layer if necessary
    if (!(desiredSelection in selectionLayers)) {
      if (desiredSelection == 'selection') {
        selectionLayers[desiredSelection] = new L.DrawingLayer();
        selectionLayers[desiredSelection].panel = leftPanel;
      } else {
        const layer = L.nonTiledLayer.nutsLayer(
            WMS_URL,
            {
              transparent: 'true',
              layers: 'area/' + desiredSelection,
              format: 'image/png',
              bounds: L.latLngBounds([-90, -180], [90, 180]),
            },
        );

        layer.setZIndex(10000);

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

    minZoomLevel = 0;

    for (let i = 0; i < layers.length; ++i) {
      const layer = layers[i];

      if (layer.visible && (layer.min_zoom_level > minZoomLevel)) {
        minZoomLevel = layer.min_zoom_level;
      }

      if (layer.leaflet_layer !== null) {
        layersToBePruned.delete(layer.leaflet_layer);
      }

      // Create the correct type of layer (if necessary)
      if (layer.visible && (layer.effect !== 'compute')) {
        if (layer.leaflet_layer === null) {
          if (layer.is_raster) {
            if (layer.is_tiled) {
              layer.leaflet_layer = L.tileLayer.wms(
                  WMS_URL,
                  {
                    transparent: 'true',
                    layers: encodeURIComponent(layer.name),
                    format: 'image/png',
                    tileSize: 256,
                    minZoom: layer.min_zoom_level,
                  },
              );
            } else {
              layer.leaflet_layer = L.nonTiledLayer.wms(
                  WMS_URL,
                  {
                    transparent: 'true',
                    layers: encodeURIComponent(layer.name),
                    format: 'image/png',
                    bounds: L.latLngBounds([-90, -180], [90, 180]),
                    pane: map.getPanes().tilePane,
                    minZoom: layer.min_zoom_level,
                  },
              );
            }
          } else {
            if (layer.is_tiled) {
              layer.leaflet_layer = L.tileLayer.queryableLayer(
                  WMS_URL,
                  {
                    transparent: 'true',
                    layers: encodeURIComponent(layer.name),
                    format: 'image/png',
                    tileSize: 256,
                    minZoom: layer.min_zoom_level,
                  },
              );
            } else {
              layer.leaflet_layer = L.nonTiledLayer.queryableLayer(
                  WMS_URL,
                  {
                    transparent: 'true',
                    layers: encodeURIComponent(layer.name),
                    format: 'image/png',
                    bounds: L.latLngBounds([-90, -180], [90, 180]),
                    pane: map.getPanes().tilePane,
                    minZoom: layer.min_zoom_level,
                  },
              );
            }
          }

          // Register to some events of the layer
          layer.leaflet_layer.on(
              'loading',
              () => {
                markLayerAsRefreshing(layer);
              },
          );

          layer.leaflet_layer.on(
              'load',
              () => {
                markLayerAsRefreshed(layer);
              },
          );

          if (layer.task_id !== null) {
            layer.leaflet_layer.on(
                layer.is_tiled ? 'tileerror' : 'error',
                () => {
                  recomputeLayer(layer, overlaysGroup);
                },
            );
          }
        }

        layer.leaflet_layer.setZIndex((layers.length - i) * 10);

        if (!overlaysGroup.hasLayer(layer.leaflet_layer)) {
          console.log('[Map] Add overlay layer: ' + layer.name);
          overlaysGroup.addLayer(layer.leaflet_layer);
        }
      } else if (layer.leaflet_layer !== null) {
        if (overlaysGroup.hasLayer(layer.leaflet_layer)) {
          console.log('[Map] Remove overlay layer: ' + layer.name);

          if (layer === highlightedLayer) {
            highlightedLayer.leaflet_layer.resetHighlightedArea();
            highlightedLayer = null;
          }

          overlaysGroup.removeLayer(layer.leaflet_layer);
        }
      }
    }

    for (const leafletLayer of layersToBePruned) {
      if ((highlightedLayer !== null) &&
          (leafletLayer === highlightedLayer.leaflet_layer)) {
        highlightedLayer.leaflet_layer.resetHighlightedArea();
        highlightedLayer = null;
      }

      overlaysGroup.removeLayer(leafletLayer);
    }

    updateZoomWarning();
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
    z-index: 0;
  }

  #findbox {
    display: inline-block;
    overflow: visible;
    vertical-align: middle;
    margin-left: 35px;
    border: 0px;
  }

  :global(#findbox input.search-input) {
    font-size: 0.9em;
    padding: 4px !important;
    min-width: 200px;
  }

  :global(#findbox .search-button) {
    background-image: url(../images/search.png);
    background-position-y: 5px;
  }

  :global(#findbox .search-button:hover) {
    background-position-y: -19px;
  }

  .warning {
    width: 300px;
    position: fixed;
    bottom: 10px;
    z-index: 100;
    left: calc((100vw - 300px) / 2);
    text-align: center;
    background-color: lightgoldenrodyellow;
    border: 1px solid #333333;
    padding: 4px;
    border-radius: 8px;
    font-size: 14px;
    background-image: url(../images/warning_icon.png);
    background-repeat: no-repeat;
    padding-left: 32px;
    background-size: 32px;
    background-position-y: center;
    background-position-x: 4px;
  }
</style>


<svelte:window on:resize={resizeMap} />

<div id="page">
  <TopNav><div id="findbox"> </div></TopNav>
  <div id="map"></div>

  {#if displayZoomWarning}
    <div class="warning">Some layers can't be displayed at this scale, zoom in to see them</div>
  {/if}
</div>
