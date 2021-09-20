<script>
  import {onMount} from 'svelte';
  import '../leaflet_components/L.TileLayer.NutsLayer.js';
  import '../leaflet_components/L.DrawingLayer.js';
  import '../leaflet_components/L.TileLayer.QueryableLayer.js';
  import {getGeofiles, WMS_URL} from '../client.js';
  import {activeSelectionLayerStore} from '../stores.js';

  // List of queryable layers that are used as selection layers.
  // The order in which they appear is mirrored in the order the layers
  // are displayed.
  export const SELECTIONS_LIST= [
    'country.geojson',
    'NUTS1.geojson',
    'NUTS2.geojson',
    'NUTS3.geojson',
    'LAU.geojson',
  ];
  export const SELECTIONS = new Set(SELECTIONS_LIST);
  let selectionLayers = [];
  let isLayerListReady = false;

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
        // We can put something else than the full name of the file
        function convertName(layer) {
          if (layer == 'country.geojson') {
            return 'Country';
          } else if (layer == 'NUTS1.geojson') {
            return 'Region NUTS1';
          } else if (layer == 'NUTS2.geojson') {
            return 'Region NUTS2';
          } else if (layer == 'NUTS3.geojson') {
            return 'Region NUTS3';
          } else if (layer == 'LAU.geojson') {
            return 'Cities';
          } else {
            return layer;
          }
        };
        leafletLayer = toNutsLayer(layer);
        leafletLayer.name = convertName(layer);
        // selection go on top
        leafletLayer.setZIndex(1000);
        selectionLayers.push(leafletLayer);
      }
    }

    selectionLayers.sort( function(layer0, layer1) {
      const areaList = [
        'Country',
        'Region NUTS1',
        'Region NUTS2',
        'Region NUTS3',
        'Cities',
      ];
      const a = areaList.indexOf(layer0.name);
      const b = areaList.indexOf(layer1.name);
      return a - b;
    });

    const drawingLayer = getDrawingLayer();
    drawingLayer.name = 'Selection';
    selectionLayers.push(drawingLayer);
    selectionLayers = selectionLayers;
    isLayerListReady = true;
  });
  function getDrawingLayer() {
    return new L.DrawingLayer();
  }
  $: {
    console.log('layer changed in selector to ' + $activeSelectionLayerStore);
  }
</script>
<style>
#map_selection {
  width: 240px;
  padding: 4px;
  border: 1px solid #27275b;
	border-radius: 0px;
  background-color: #eff4fa !important;
  box-sizing: border-box;
}
#map_selection h3 {
  margin: 0px;
  height: 25px;
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

label {
  display: block;
  overflow-y: auto;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow-x: hidden;
  margin-top: 2px;
}
</style>

<div id="map_selection" on:click|stopPropagation on:wheel|stopPropagation>
  {#if !isLayerListReady}
  Loading layers...
  {:else}
  <h3>Area selection</h3>
  <div id="selection_layers">
  {#each selectionLayers as selectionLayer}
  <label title={selectionLayer.name}>
    <input type=radio bind:group={$activeSelectionLayerStore} value={selectionLayer}>
    {selectionLayer.name}
  </label>
  {/each}
  </div>
  {/if}
</div>
