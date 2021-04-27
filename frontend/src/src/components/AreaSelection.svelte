<script>
    /*  CE SCRIPT CONTIENT EN FAIT LA SELECTION DES CALQUES QU'ON RAJOUTE POUR FAIRE LES CALCULS*/
    
    import {onMount} from 'svelte';
    import '../leaflet_components/L.TileLayer.NutsLayer.js';
    import '../leaflet_components/L.DrawingLayer.js';
    import '../leaflet_components/L.TileLayer.QueryableLayer.js';
    import queryString from 'query-string';
    import {getGeofiles, WMS_URL} from '../client.js';
    import {activeOverlayLayersStore} from '../stores.js';
  
    // List of queryable layers that are used as selection layers.
    // The order in which they appear is mirrored in the order the layers are displayed.
    let overlayLayers = [];
    let isLayerListReady = false;
  
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

    onMount(async () => {
      const layers = await getGeofiles();
      for (const [layer, layerParameters] of Object.entries(layers)) {
        let leafletLayer;
        console.log(layer, layerParameters);

        if (!layerParameters.isQueryable) {
          leafletLayer = toOverlayLayer(layer);
          leafletLayer.name = layer;
          overlayLayers.push(leafletLayer);
        }
      }

      overlayLayers = overlayLayers;
      // Add all the overlay layers
      setSelectionFromGetParameter();
      isLayerListReady = true;
    });
    function setSelectionFromGetParameter() {
      const parsed = queryString.parse(window.location.search);
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

    $: {
      console.log('layer changed in selector to ' + $activeOverlayLayersStore);
    }
  </script>
  
  <style>
    
  #map_selection {
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
    overflow-y: auto;
    border : none;
  }
  
  </style>
  
  <div id="map_selection"  on:click|stopPropagation="">
    {#if !isLayerListReady}
    Loading layers...
    {:else}
    <h3>Active Layers Selection</h3>
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
  