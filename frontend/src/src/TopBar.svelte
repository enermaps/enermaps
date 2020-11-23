<script>
	import { onMount } from 'svelte';
	import './L.TileLayer.NutsLayer.js'
	import './L.DrawingLayer.js'
	export const SELECTIONS = new Set(['lau.zip', 'nuts0.zip', 'nuts1.zip', 'nuts2.zip' ,'nuts3.zip'])
	export let selection_layers = [];
	export let active_selection_layer = undefined;
	export let overlay_layers = [];
	export let active_overlay_layers = [];
	let test = [];
	let layer_count = 0

	onMount(async () => {
		const layers = await fetchLayers();
		for (const layer of layers) {
			const leaflet_layer = to_leaflet_layer(layer);
			leaflet_layer.name = layer;
			if (SELECTIONS.has(layer)) {
				selection_layers.push(leaflet_layer);
			} else {
				overlay_layers.push(leaflet_layer);
			}
		}
		let drawing_layer = get_drawing_layer();
		drawing_layer.name = "selection";
		selection_layers.push(drawing_layer);
		selection_layers = selection_layers;
		console.log(selection_layers);
		overlay_layers = overlay_layers;
		console.log(overlay_layers);
	});
	async function fetchLayers() {
		//document.domain = "geoserver.hotmaps.eu";
		let response = await fetch('/api/geofile');
		if (!response.ok) {
			console.log(err);
			return [];
		}
		let layers_resp = await response.json();
		return layers_resp.files;
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
	function get_drawing_layer() {
		return new L.DrawingLayer();
	}
</script>
<div>
	{#each overlay_layers as overlay_layer}
	<label>
		<input type=checkbox bind:group={active_overlay_layers} value={overlay_layer}>
			{overlay_layer.name}
		</label>
	{/each}

	{#each selection_layers as selection_layer}
	<label>
		<input type=radio bind:group={active_selection_layer} value={selection_layer}>
		{selection_layer.name}
	</label>
	{/each}
</div>
