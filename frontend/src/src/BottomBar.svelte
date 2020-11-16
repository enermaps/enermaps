<script>
	import { afterUpdate, onMount } from 'svelte';
	import 'brutusin-json-forms'
	export let active_overlay_layers;
	export let active_selection_layer;
	let brutusin_forms = {};
	const BrutusinForms = brutusin["json-forms"];
	let cms =[];
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
			if (!(cm.name in brutusin_forms)) {
				const container = document.getElementById('form' + cm.name);
				console.log(cm);
				const form = BrutusinForms.create(cm.schema);
				form.render(container, {});
				brutusin_forms[cm.name] = form;
			}
		}
	});
	async function callCM(cm_name) {
		//alert("calling CM with overlays :" + active_overlay_layers + "and with selection:" + active_selection_layer)
		let data = {}
		data['selection'] = active_selection_layer.getSelection();
		data['overlays'] = active_overlay_layers;
		data['input'] = brutusin_forms[cm_name].getData();
		const response = await fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data),
		});
	}
	$ : {
		console.log(`selected layer was changed: ${active_selection_layer}`);
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
