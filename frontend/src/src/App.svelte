<script>
import CMList from './components/CMList.svelte';
import Map from './components/Map.svelte';

let activeSelectionLayer = undefined;
let activeOverlayLayers = [];


</script>

<style>
body {
	margin-bottom: 20px;
	width: 100%;
	height: 100%;
}
</style>
<Map bind:activeSelectionLayer bind:activeOverlayLayers/>
<CMList bind:activeSelectionLayer bind:activeOverlayLayers/>
