<script>
import CMList from './components/CMList.svelte';
import Map from './components/Map.svelte';

let active_selection_layer = undefined;
let active_overlay_layers = [];


</script>

<style>
body {
	margin-bottom: 20px;
	width: 100%;
	height: 100%;
}
</style>
<Map bind:active_selection_layer bind:active_overlay_layers/>
<CMList bind:active_selection_layer bind:active_overlay_layers/>
