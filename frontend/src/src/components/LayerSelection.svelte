<script>

  /* CE FICHIER CONTIENT EN FAIT LA SELECTION DES ZONES POUR LES CALCULS*/
  
  import {onMount} from 'svelte';
  import '../leaflet_components/L.TileLayer.NutsLayer.js';
  import '../leaflet_components/L.DrawingLayer.js';
  import '../leaflet_components/L.TileLayer.QueryableLayer.js';
  import queryString from 'query-string';
  import {getGeofiles, WMS_URL} from '../client.js';
  import {activeSelectionLayerStore} from '../stores.js';

  // List of queryable layers that are used as selection layers.
  // The order in which they appear is mirrored in the order the layers are displayed.
  // If the names are changed, the list isn't of layers isn't loading...why?
  export const SELECTIONS_LIST= [
    'nuts0.zip',
    'nuts1.zip',
    'nuts2.zip',
    'nuts3.zip',
    'lau.zip',
  ];
  export const SELECTIONS = new Set(SELECTIONS_LIST);
  let selectionLayers = [];
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
        // NUTS and LAU layers
        leafletLayer = toNutsLayer(layer);
        leafletLayer.name = layer;
        // selection go on top
        leafletLayer.setZIndex(1000);
        selectionLayers.push(leafletLayer);
      } else if (layerParameters.isQueryable) {
        leafletLayer = toQueryableLayer(layer);
        leafletLayer.name = layer;
        overlayLayers.push(leafletLayer);
      }
    }

    // Sort layers by name
    function compareSelectionLayer(layer0, layer1) {
      const layer0Name = layer0.name;
      const layer1Name = layer1.name;
      return SELECTIONS_LIST.indexOf(layer0Name) > SELECTIONS_LIST.indexOf(layer1Name);
    }
    // Sort the layer list by name
    selectionLayers.sort(compareSelectionLayer);
  
    // Add the layer for custom selection - we get a new layer from leaflet
    const drawingLayer = getDrawingLayer();
    drawingLayer.name = 'Custom area';
    // Add the custom selection layer at the end of the list
    selectionLayers.push(drawingLayer);
    selectionLayers = selectionLayers;
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
  }

  function getDrawingLayer() {
    return new L.DrawingLayer();
  }

  $: {
    console.log('layer changed in selector to ' + $activeSelectionLayerStore);
  }
</script>

<style>
  
#map_selection {
  padding: 4px;
  border: 1px solid #27275b;
	border-radius: 0px;
  background-color: #eff4fa;
  width: 100%;
  box-sizing: border-box;
}

#map_selection h3 {
  margin: 0px;
  height: 40%;
  display: flex;
  flex-direction: column;
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

</style>

<div id="map_selection" on:click|stopPropagation="">
  {#if !isLayerListReady}
  Loading areas...
  {:else}
  <h3>Area Selection</h3>
  <div id="selection_layers">
  {#each selectionLayers as selectionLayer}
  <label>
    <input type=radio bind:group={$activeSelectionLayerStore} value={selectionLayer}>
    {selectionLayer.name}
  </label>
  {/each}
  </div>

  {/if}
</div>
