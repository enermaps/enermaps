<script>
	import { onMount } from 'svelte';
	import './L.TileLayer.NutsLayer.js'
	export let layers = [];
	export let activated_layer;
	export let search; 
	let layer_count = 0
	onMount(async () => {
		layers = await fetchLayers();
	});
	async function fetchLayers() {
		//document.domain = "geoserver.hotmaps.eu";
		let response = await fetch('http://127.0.0.1:7000/api/geofile/');
		if (!response.ok) {
			console.log(err);
			return [];
		}
		var layers_resp = await response.json();
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
	function activateLayer(layer) {
		activated_layer = layer;
	}
	function removeLayer(layer) {
	}
</script>
<div>
	<input bind:value={search}>
	{#each layers as layer}
	<button on:click={() => activateLayer(layer)}>
			Activate {layer.options.layers}
		</button>
	{/each}
</div>
