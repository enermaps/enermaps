<script>
  import {onMount} from 'svelte';
  import '../leaflet_components/L.TileLayer.NutsLayer.js';
  import '../leaflet_components/L.DrawingLayer.js';
  import '../leaflet_components/L.TileLayer.QueryableLayer.js';
  import queryString from 'query-string';
  import {getGeofiles, WMS_URL} from '../client.js';
  import {activeOverlayLayersStore, activeSelectionLayerStore} from '../stores.js';

  // List of queryable layers that are used as selection layers.
  // The order in which they appear is mirrored in the order the layers
  // are displayed.
  export const SELECTIONS_LIST= [
    'nuts0.zip',
    'nuts1.zip',
    'nuts2.zip',
    'nuts3.zip',
    'lau.zip',
  ];
  export const SELECTIONS = new Set(SELECTIONS_LIST);
  let selectionLayers = [];
  // export let activeSelectionLayer = ;
  let overlayLayers = [];
  // export let activeOverlayLayers = $activeOverlayLayersStore;
  let isLayerListReady = false;

  function toQueryableLayer(layerName) {
    const layer = L.tileLayer.queryableLayer(
        WMS_URL,
        {
          transparent: 'true',
          layers: layerName,
          format: 'image/png',
        },
    );
    return layer;
  }

  function toOverlayLayer(layerName) {
    const layer = L.tileLayer.wms(
        WMS_URL,
        {
          transparent: 'true',
          layers: layerName,
          format: 'image/png',
        },
    );
    return layer;
  }

  function toNutsLayer(layerName) {
    const layer = L.tileLayer.nutsLayer(
        WMS_URL,
        {
          transparent: 'true',
          layers: layerName,
          format: 'image/png',
        },
    );
    return layer;
  }
  onMount(async () => {
    const layers = await getGeofiles();
    for (const [layer, layerParameters] of Object.entries(layers)) {
      let leafletLayer;
      console.log(layer, layerParameters);
      if (SELECTIONS.has(layer)) {
        leafletLayer = toNutsLayer(layer);
        leafletLayer.name = layer;
        // selection go on top
        leafletLayer.setZIndex(1000);
        //
        selectionLayers.push(leafletLayer);
      } else if (layerParameters.isQueryable) {
        leafletLayer = toQueryableLayer(layer);
        leafletLayer.name = layer;
        overlayLayers.push(leafletLayer);
      } else {
        leafletLayer = toOverlayLayer(layer);
        leafletLayer.name = layer;
        overlayLayers.push(leafletLayer);
      }
    }
    function compareSelectionLayer(layer0, layer1) {
      const layer0Name = layer0.name;
      const layer1Name = layer1.name;
      return SELECTIONS_LIST.indexOf(layer0Name) > SELECTIONS_LIST.indexOf(layer1Name);
    }
    selectionLayers.sort(compareSelectionLayer);
    const drawingLayer = getDrawingLayer();
    drawingLayer.name = 'selection';
    selectionLayers.push(drawingLayer);
    selectionLayers = selectionLayers;
    overlayLayers = overlayLayers;
    setSelectionFromGetParameter();
    isLayerListReady = true;
  });
  function setSelectionFromGetParameter() {
    const parsed = queryString.parse(window.location.search);
    if ('selectionLayer' in parsed) {
      let activeSelectionLayer = undefined;
      console.log('parsing selection layer from get parameters');
      for (const selectionLayer of selectionLayers) {
        if (selectionLayer.name == parsed.selectionLayer) {
          console.log('adding selection layer from get parameters');
          activeSelectionLayer = selectionLayer;
        }
      }
      $activeSelectionLayerStore = activeSelectionLayer;
    }
    if ('overlayLayers' in parsed) {
      const activeOverlayLayers = [];
      console.log('parsing overlay layer from get parameters');
      const queryOverlayLayers = new Set(parsed.overlayLayers.split(','));
      for (const overlayLayer of overlayLayers) {
        if (queryOverlayLayers.has(overlayLayer.name)) {
          console.log('adding overlay layer from get parameters');
          activeOverlayLayers.push(overlayLayer);
        }
      }
      $activeOverlayLayersStore = activeOverlayLayers;
    }
  }
  function getDrawingLayer() {
    return new L.DrawingLayer();
  }
  $: {
    console.log('layer changed in selector to ' + $activeSelectionLayerStore);
    console.log('layer changed in selector to ' + $activeOverlayLayersStore);
  }
</script>

<style>
  
#map_selection {
  padding: 4px;
  border: 1px solid #27275b;
	border-radius: 0px;
  background-color: #eff4fa;
}


#map_selection h3 {
  margin: 0px;
  height: 40%;
  display: flex;
  flex-direction: column;
  max-width: 200px;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden !important;
}

h3 {
  flex-shrink: 0;
  border : none;
}
#selection_layers {
  overflow-y: auto;
  border : none;

}
#overlay_layers {
  overflow-y: auto;
  border : none;
}

</style>

<div id="map_selection" on:click|stopPropagation="">
  {#if !isLayerListReady}
  Loading layers
  {:else}
  <h3>Selection</h3>
  <div id="selection_layers">
  {#each selectionLayers as selectionLayer}
  <label>
    <input type=radio bind:group={$activeSelectionLayerStore} value={selectionLayer}>
    {selectionLayer.name}
  </label>
  {/each}
  </div>

  <h3>Overlays</h3>
  <div id="overlay_layers">
  {#each overlayLayers as overlayLayer}
  <label>
    <input type=checkbox bind:group={$activeOverlayLayersStore} value={overlayLayer}>
      {overlayLayer.name}
    </label>
  {/each}
  </div>

  {/if}
</div>
