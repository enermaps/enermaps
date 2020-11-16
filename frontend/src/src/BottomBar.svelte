<script>
	import { onMount } from 'svelte';
	export let active_overlay_layers;
	export let active_selection_layer;
	let cms = {}
	onMount(async() => {
		cms = await fetchCMs();
	});

	async function fetchCMs() {
		let response = await fetch('/api/cm/');
		if (!response.ok) {
			console.log(response);
			return [];
		}
		let cms_resp = await response.json();
		return cms_resp.cms;
	}
	async function callCM(cm_name) {
		alert("calling CM with overlays :" + active_overlay_layers + "and with selection:" + active_selection_layer)
	}
</script>

<footer class="page-footer grey darken-4">
	Call a calculation module
	<ul>
	{#each cms as cm}
	<li>
	<button on:click={() => callCM(cm.name)}>{cm.name}</button>
	</li>
	{/each}
	</ul>
</footer>
