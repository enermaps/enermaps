<script>
	// Import CSS from Leaflet and plugins.
	import 'leaflet/dist/leaflet.css';
	import 'leaflet.markercluster/dist/MarkerCluster.css';
	import 'leaflet.markercluster/dist/MarkerCluster.Default.css';

	// Import images directly that got missed via the CSS imports above.
	//import 'leaflet/dist/images/marker-icon-2x.png';
	//import 'leaflet/dist/images/marker-shadow.png';

	// Import JS from Leaflet and plugins.
	import 'leaflet/dist/leaflet';
	import 'leaflet.markercluster/dist/leaflet.markercluster';
	import 'leaflet.gridlayer.googlemutant/Leaflet.GoogleMutant';
	import "leaflet-search/dist/leaflet-search.src.js"
	import "leaflet-search/dist/leaflet-search.src.css"

	import { onMount } from 'svelte';
	import TopBar from './TopBar.svelte';
	import BottomBar from './BottomBar.svelte';

	let map;
	let active_selection_layer = undefined;
	let active_overlay_layers = [];
	let search = "";
	let base_layers = new Set();
	onMount(async() => {
		console.log("init map");
		map = L.map('map').setView([51.505, -0.09], 13);
		const base_layer = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy;' +
    ' <a href="https://cartodb.com/attributions">CartoDB</a>'
  });

		base_layer.addTo(map);
		base_layers.add(base_layer);
		map.addControl(getSearchControl());
	});

	function resizeMap() {
		if(map) { map.invalidateSize(); }
	}

	$: {
		console.log(`selected layer was changed: ${active_selection_layer}`)
		removeAllLayer();
		if (!!active_selection_layer) {
			active_selection_layer.addTo(map)
		}
		for (const overlay_layer of active_overlay_layers) {
			overlay_layer.addTo(map)
		}
	}
	function removeAllLayer() {
		if (!!!map) {
			return;
		}
		map.eachLayer(function (layer) {
			if (!base_layers.has(layer)) {
			    map.removeLayer(layer);
			}
		});
	}
	function getSearchControl() {
		const search_control = new L.Control.Search({
			url: 'https://nominatim.openstreetmap.org/search?format=json&q={s}',
			jsonpParam: 'json_callback',
			propertyName: 'display_name',
			propertyLoc: ['lat', 'lon'],
			marker: false, // L.circleMarker([0, 0], { radius: 30 }),
			autoCollapse: true,
			autoType: false,
			minLength: 2,
		});
		return search_control;
	}
</script>

<style>
#map { 
	width: 100%;
	height: 100%;
}
body {
	margin-bottom: 20px;
}
</style>
<svelte:window on:resize={resizeMap} />
<TopBar bind:active_selection_layer={active_selection_layer} bind:active_overlay_layers={active_overlay_layers}/>
{#if search}
<br/>
search is {search}
{/if}
<div id="map">
</div>
<BottomBar bind:active_selection_layer={active_selection_layer} bind:active_overlay_layers={active_overlay_layers}/>
