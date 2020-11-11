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

	import { onMount } from 'svelte';
	import TopBar from './TopBar.svelte';

	let map;
	let selection_layer;
	let search = "";
	onMount(async() => {
		map = L.map('map').setView([51.505, -0.09], 13);

		const layer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
		}).addTo(map);
	});

	$: {
		console.log(`selected layer was changed: ${selection_layer}`)
		removeAllLayer();
		if (selection_layer !== undefined) {
		  selection_layer.addTo(map);
		}
	}
	function removeAllLayer() {
		if (!!!map) {
			return;
		}
		map.eachLayer(function (layer) {
		    map.removeLayer(layer);
		});
	}
</script>

<style>
#map { 
	width: 100%;
	height: 100%;
}
</style>
<TopBar bind:selection_layer={selection_layer}/>
{#if search}
<br/>
search is {search}
{/if}
<div id="map">
</div>
