<script>
  import {onMount} from 'svelte';
  import '../leaflet_components/L.TileLayer.NutsLayer.js';
  import '../leaflet_components/L.DrawingLayer.js';
  import '../leaflet_components/L.TileLayer.QueryableLayer.js';
  import queryString from 'query-string';
  import {getGeofiles, getLegend, getOpenairLink, WMS_URL} from '../client.js';
  import {activeOverlayLayersStore, activeSelectionLayerStore} from '../stores.js';

  let selectionLayers = [];
  let overlayLayers = [];

  let isLayerListReady = false;
  let overlayLayersFilter = '';
  let filteredOverlayLayers = [];
  export const SELECTIONS_LIST= [
    'country.geojson',
    'NUTS1.geojson',
    'NUTS2.geojson',
    'NUTS3.geojson',
    'LAU.geojson',
  ];
  export const SELECTIONS = new Set(SELECTIONS_LIST);

  function toQueryableLayer(layerName) {
    const layer = L.tileLayer.queryableLayer(
        WMS_URL,
        {
          transparent: 'true',
          layers: encodeURIComponent(layerName),
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
          layers: encodeURIComponent(layerName),
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
      if (!SELECTIONS.has(layer)) {
        let legend;
        legend = getLegend(layer);
        console.log(legend);

        let openairLink;
        openairLink = getOpenairLink(layer);
        console.log(openairLink);

        if (layerParameters.isQueryable) {
          leafletLayer = toQueryableLayer(layer);
        } else {
          leafletLayer = toOverlayLayer(layer);
        }

        leafletLayer.name = layer;
        leafletLayer.legend_promise = legend;
        leafletLayer.openairLink_promise = openairLink;

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
    filteredOverlayLayers = overlayLayers;
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
    filteredOverlayLayers = overlayLayers.filter((layer) =>
      layer.name.indexOf(overlayLayersFilter) !== -1);
  }
</script>

  <style>

  #map_selection {
    width: 140px;
    padding: 4px;
    border: 1px solid #27275b;
    border-radius: 0px;
    background-color: #eff4fa;
    box-sizing: border-box;
    width: 100%;
  }

  #map_selection h3 {
    margin: 0px;
    height: 40%;
    width: 100%;
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
  #overlay_layers {
    width: 140px;
    overflow-y: auto;
    border : none;
  }

  label {
  display: block;
  overflow-y: auto;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow-x: hidden;
  }
  .overlay_search {
    width: 100%;
  }

  .box {
  /* float: left; */
  height: 10px;
  width: 10px;
  /* margin-bottom: 15px; */
  border: 1px solid black;
  /* clear: both; */
  display: inline-block;
  }

  #metadata_box {
    border: 1px solid #27275b;
    border-radius: 0px;
    background-color: #fff;
    padding: 5px;
  }

  </style>
  <div id="map_selection" on:click|stopPropagation="">
    {#if !isLayerListReady}
    Loading layers...
    {:else}
    <h3>Overlays</h3>
    <div id="overlay_layers">
    Filter: <input bind:value={overlayLayersFilter} class="overlay_search">
    {#each filteredOverlayLayers as overlayLayer (overlayLayer.name)}
    <label title={overlayLayer.name}>
      <input type=checkbox bind:group={$activeOverlayLayersStore} value={overlayLayer}>
        {overlayLayer.name}
    </label>

    <div id="metadata_box">
      {#await overlayLayer.legend_promise}
        <div>...waiting for legend</div>
      {:then legend}
        <div>{legend.variable.variable}</div>
        {#each legend.style as color}
          <div style="display: inline-block;">
            <div class='box' style="background-color: rgb( {color[0][0]}, {color[0][1]}, {color[0][2]} )"> </div>
            <div style="display: inline-block;">{color[1]} to {color[2]} {legend.variable.units}</div>
          </div>
        {/each}

      {:catch error}
        <div style="color: red">{error.message}</div>
      {/await}

      {#await overlayLayer.openairLink_promise}
      <div>...waiting for OpenAir link</div>
      {:then openairLink}
        <div>
          <a href={openairLink} target="_blank">OpenAir link &#128279;</a>
        </div>
      {:catch error}
        <div style="color: red">{error.message}</div>
      {/await}
    </div>


    {/each}
    </div>

    {/if}
  </div>
