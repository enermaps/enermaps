<script>
	import { onMount } from 'svelte';
	export let active_overlay_layers;
	export let active_selection_layer;
	let cms = []
	onMount(async() => {
		cms = await fetchCMs();
	});

	async function fetchCMs() {
		let response = await fetch('/api/cm/');
		if (!response.ok) {
			console.log(err);
			return [];
		}
		let cms_resp = await response.json();
		return cms_resp.cms;
	}
	async function callCM() {
	console.log(active_overlay_layers);
	console.log(active_selection_layer);

	}
</script>

<footer class="page-footer grey darken-4">
	{#each cms as cm}
	{cm}
	{/each}
</footer>
