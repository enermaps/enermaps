<script>
	import { afterUpdate, onMount } from 'svelte';
	import 'brutusin-json-forms'
	export let active_overlay_layers;
	export let active_selection_layer;
	const BrutusinForms = brutusin["json-forms"];
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
	afterUpdate(async() =>{
		for (const cm of cms) {
			console.log(cm)
			const form = BrutusinForms.create(cm.schema)
			const container = document.getElementById('form' + cm.name);
			form.render(container, {})
		}
	});
	async function callCM(cm_name) {
		//alert("calling CM with overlays :" + active_overlay_layers + "and with selection:" + active_selection_layer)
		alert(active_selection_layer.getSelection())
	}
	function handleReset() {
	}
</script>

<footer class="page-footer grey darken-4">
	Call a calculation module
	<ul>
	{#each cms as cm}
	<li>
		<form id="form{cm.name}">
		</form>
		<button type=submit on:click={() => callCM(cm.name)}>{cm.name}</button>
	</li>
	{/each}
	</ul>
</footer>
