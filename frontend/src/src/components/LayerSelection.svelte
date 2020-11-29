<script>
  import {onMount} from 'svelte';
  import '../leaflet_components/L.TileLayer.NutsLayer.js';
  import '../leaflet_components/L.DrawingLayer.js';
  import queryString from 'query-string';
  import {getGeofiles, WMS_URL} from '../client.js';

  export const SELECTIONS = new Set(['lau.zip', 'nuts0.zip', 'nuts1.zip', 'nuts2.zip', 'nuts3.zip']);
  let selectionLayers = [];
  export let activeSelectionLayer = undefined;
  let overlayLayers = [];
  export let activeOverlayLayers = [];

  function toLeafletLayer(layerName) {
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
    for (const layer of layers) {
      const leafletLayer = toLeafletLayer(layer);
      leafletLayer.name = layer;
      if (SELECTIONS.has(layer)) {
        // selection go on top
        leafletLayer.setZIndex(1000);
        selectionLayers.push(leafletLayer);
      } else {
        overlayLayers.push(leafletLayer);
      }
    }
    const drawingLayer = getDrawingLayer();
    drawingLayer.name = 'selection';
    selectionLayers.push(drawingLayer);
    selectionLayers = selectionLayers;
    overlayLayers = overlayLayers;
    setSelectionFromGetParameter();
  });
  function setSelectionFromGetParameter() {
    if (!!!window) {
      return;
    }
    const parsed = queryString.parse(window.location.search);
    if ('selectionLayer' in parsed) {
      console.log('parsing selection layer from get parameters');
      for (const selectionLayer of selectionLayers) {
        if (selectionLayer.name == parsed.selectionLayer) {
          console.log('adding selection layer from get parameters');
          activeSelectionLayer = selectionLayer;
        }
      }
    }
    if ('overlayLayers' in parsed) {
      console.log('parsing overlay layer from get parameters');
      const queryOverlayLayers = new Set(parsed.overlayLayers.split(','));
      for (const overlayLayer of overlayLayers) {
        if (queryOverlayLayers.has(overlayLayer.name)) {
          console.log('adding overlay layer from get parameters');
          activeOverlayLayers.push(overlayLayer);
        }
      }
    }
    // trigger the modification of the overlay layers to the
    // parent component
    activeOverlayLayers = activeOverlayLayers;
  }
  function getDrawingLayer() {
    return new L.DrawingLayer();
  }
</script>
<style>
#map_selection {
  border-style: groove;
}
</style>
<div id="map_selection">
  {#each overlayLayers as overlayLayer}
  <label>
    <input type=checkbox bind:group={activeOverlayLayers} value={overlayLayer}>
      {overlayLayer.name}
    </label>
  {/each}

  {#each selectionLayers as selectionLayer}
  <label>
    <input type=radio bind:group={activeSelectionLayer} value={selectionLayer}>
    {selectionLayer.name}
  </label>
  {/each}
</div>
