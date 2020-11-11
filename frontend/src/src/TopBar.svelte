<script>
	import { onMount } from 'svelte';
	import './L.TileLayer.NutsLayer.js'
	import './L.DrawingLayer.js'
	export let selection_layers = [];
	export let selection_layer;
	let layer_count = 0
	onMount(async () => {
		selection_layers = await fetchLayers();
		selection_layers.push(getDrawingLayer());
	});
	async function fetchLayers() {
		//document.domain = "geoserver.hotmaps.eu";
		let response = await fetch('http://127.0.0.1:7000/api/geofile/');
		if (!response.ok) {
			console.log(err);
			return [];
		}
		let layers_resp = await response.json();
		return layers_resp.files.map(to_leaflet_layer);
	}
	function to_leaflet_layer(layer_name) {
	  const layer =  L.tileLayer.nutsLayer(
	      'http://127.0.0.1:7000/api/wms?',
	      {
		transparent: 'true',
		layers: layer_name,
			format: 'image/png',
	      },
		  );
		return layer;
	}
	function getDrawingLayer() {
		return new L.DrawingLayer();
	}
	function activateLayer(layer) {
		selection_layer = layer;
	}
	function removeLayer(layer) {
	}
</script>
<div>
	{#each selection_layers as layer}
	<button on:click={() => activateLayer(layer)}>
			Activate {layer.options.layers}
		</button>
	{/each}
</div>
