<script>
  import {onMount} from 'svelte';
  import '../leaflet_components/L.TileLayer.QueryableLayer.js';
  import {getGeofiles, getLegend, getLayerType, getOpenairLink, WMS_URL} from '../client.js';
  import {activeOverlayLayersStore} from '../stores.js';

  const activeOverlayLayers = [];
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

  function splitName(name) {
    return name.substring(3).replace(/\.[^/.]+$/, '');
  };


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
        const legend = getLegend(layer);
        console.log(legend);
        const layerType = getLayerType(layer);
        console.log(layerType);

        const openairLink = getOpenairLink(layer);
        console.log(openairLink);

        if (layerParameters.isQueryable) {
          leafletLayer = toQueryableLayer(layer);
        } else {
          leafletLayer = toOverlayLayer(layer);
        }

        leafletLayer.name = layer;
        leafletLayer.datasetId = parseInt(layer.substring(0, 2));
        leafletLayer.legend_promise = legend;
        leafletLayer.openairLink_promise = openairLink;
        leafletLayer.layer_type_promise = layerType;
        overlayLayers.push(leafletLayer);

        // select if dataset to show is set in the URL
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('datasetId')) {
          const datasetSelected = parseInt(urlParams.get('datasetId'));
          if (leafletLayer.datasetId == datasetSelected) {
            leafletLayer.checked = true;
            activeOverlayLayers.push(leafletLayer);
          }
        }
      }
    }

    // we can now push the potential selected dataset
    $activeOverlayLayersStore = activeOverlayLayers;

    overlayLayers.sort(function(layer0, layer1) {
      const name0 = splitName(layer0.name);
      const name1 = splitName(layer1.name);
      if (name0 < name1) {
        return -1;
      }
      if (name0 > name1) {
        return 1;
      }
      return 0;
    });
    overlayLayers = overlayLayers;
    filteredOverlayLayers = overlayLayers;
    isLayerListReady = true;
  });
  $: {
    console.log('layer changed in selector to ' + $activeOverlayLayersStore);
    filteredOverlayLayers = overlayLayers.filter((layer) =>
      layer.name.toLowerCase().indexOf(overlayLayersFilter.toLowerCase()) !== -1);
  }
</script>

  <style>

  #map_selection {
    width: 240px;
    padding: 4px;
    border: 1px solid #27275b;
    border-radius: 0px;
    background-color: #eff4fa;
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

  #overlay_layers {
    max-height: 300px;
    overflow-y: auto;
    border : none;
    overflow-y: scroll;
    scrollbar-color: #27275b;
    scrollbar-width: thin;
  }

  label {
  display: block;
  overflow-y: auto;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow-x: hidden;
  margin-top: 2px;
  }
  .overlay_search {
    width: 100%;
  }

  .box {
    height: 10px;
    width: 10px;
    border: 1px solid black;
    display: inline-block;
  }

  #metadata_box {
    border: 1px solid #27275b;
    border-radius: 0px;
    background-color: #fff;
    padding: 5px;
    width: inherit;
    margin-right: 10px;
    margin-left: 10px;
    overflow: hidden;
  }

  </style>
  <div id="map_selection" on:click|stopPropagation="">
    {#if !isLayerListReady}
    Loading layers...
    {:else}
    <h3>Overlays layers</h3>
      <input bind:value={overlayLayersFilter} class="overlay_search" placeholder="Search layer...">
    <div id="overlay_layers" style="margin-top: 10px;">

    {#each filteredOverlayLayers as overlayLayer (overlayLayer.name)}
    <label title={splitName(overlayLayer.name)}>
      <input type=checkbox bind:group={$activeOverlayLayersStore} value={overlayLayer} bind:checked={overlayLayer.checked}>
        {splitName(overlayLayer.name)}
    </label>

    <div id="metadata_box" hidden={!overlayLayer.checked}>
      {#await overlayLayer.legend_promise}
        <div>...waiting for legend</div>
      {:then legend}
        <div><b>{legend.variable.variable}</b></div>
        <div>
        {#each legend.style as color}
          <div style="display: inline-block;">
            {#await overlayLayer.layer_type_promise}
              <div>...waiting for data_type</div>
            {:then layerType}
              {#if layerType.data_type == 'categorical'}
                <div class='box' style="background-color: rgb( {color[1][0][0]}, {color[1][0][1]}, {color[1][0][2]} )"> </div>
                <div style="display: inline-block;">{color[1][1]}</div><br>
              {:else}
                <div class='box' style="background-color: rgb( {color[0][0]}, {color[0][1]}, {color[0][2]} )"> </div>
                <div style="display: inline-block;">{color[1].toFixed(2)} to {color[2].toFixed(2)} {legend.variable.units}</div><br>
              {/if}
            {/await}

          </div>
        {/each}
        </div>

      {:catch error}
        <div style="color: red">{error.message}</div>
      {/await}

      {#await overlayLayer.openairLink_promise}
      <div>...waiting for OpenAIRE link</div>
      {:then openairLink}
        <div>
          <a href={openairLink} target="_blank">Link to OpenAIRE metadata &#128279;</a>
        </div>
      {:catch error}
        <div style="color: red">{error.message}</div>
      {/await}
    </div>


    {/each}
    </div>

    {/if}
  </div>
