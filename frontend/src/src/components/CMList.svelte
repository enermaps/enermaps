<script>
	import { afterUpdate, onMount } from 'svelte';

	import CMResult from './CMResult.svelte';
	import { BASE_URL } from '../settings.js'
	import 'brutusin-json-forms'
	export let active_overlay_layers;
	export let active_selection_layer;
	let disabled = true;
	let brutusin_forms = {};
	const BrutusinForms = brutusin["json-forms"];
	let cms =[];
	let cm_tasks =[];
	onMount(async() => {
		cms = await fetchCMs();
	});

	async function fetchCMs() {
		let response = await fetch(BASE_URL + 'api/cm/');
		if (!response.ok) {
			return [];
		}
		let cms_resp = await response.json();
		return cms_resp.cms;
	}
	afterUpdate(async() =>{
		for (const cm of cms) {
			if (!(cm.name in brutusin_forms)) {
				const container = document.getElementById('form' + cm.name);
				const form = BrutusinForms.create(cm.schema);
				form.render(container);
				brutusin_forms[cm.name] = form;
			}
		}
	});
	async function callCM(cm) {
		//alert("calling CM with overlays :" + active_overlay_layers + "and with selection:" + active_selection_layer)
		let new_task_params = {}
		const cm_name = cm.name;
		if (!!active_selection_layer) {
			new_task_params['selection'] = active_selection_layer.getSelection();
		} else {
			new_task_params['selection'] = {}
		}
		new_task_params['layers'] = active_overlay_layers.map(layer=>layer.name);
		new_task_params['parameters'] = brutusin_forms[cm_name].getData();
		console.log(new_task_params);
		const response = await fetch(BASE_URL + "api/cm/" + cm_name + "/task", {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(new_task_params),
		});
		const task = await response.json()
		cm_tasks.push({"cm": cm, "task_id": task.task_id});
		cm_tasks = cm_tasks;
	}
	$ : {
		console.log(`selected layer was changed: ${active_selection_layer}`);
		disabled = !active_overlay_layers.length || !active_selection_layer;

	}
	function handleReset() {
	}
</script>
<style>
#calculation_modules {
	border-style: groove;
}
</style>
<div id="calculation_modules">
	Call a calculation module
	<ul>
	{#each cms as cm}
	<li>
		<form id="form{cm.name}">
		</form>
		<button type=submit on:click={() => callCM(cm)} disabled={disabled}>{cm.pretty_name}</button>
	</li>
	{/each}
	</ul>
	{#each cm_tasks as cm_task}
		<CMResult task={cm_task}/>
	{/each}
</div>
