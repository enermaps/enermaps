<script>
	import { onMount } from 'svelte';
	export let task;
	let task_status;
	let is_task_pending = true;
	const update_time = 500;

	onMount(async() => {
		getTaskResult();
	});
	function isTaskPending() {
		if (!task_status) {
			return true;
		}
		return task_status.status === 'PENDING';
	}
	async function getTaskResult() {
		const task_response = await fetch('/api/cm/' + task.cm.name + '/task/' + task.task_id);
		const task_json= await task_response.json();
		task_status = task_json;
		if (task_status.status === 'PENDING') {
		    setTimeout(getTaskResult, 500);
		} else {
			is_task_pending = false;
		}
	}
	async function cancel() {
		const cancel_response = await fetch('/api/cm/' + task.cm.name + '/task/' + task.task_id, {
			method: 'DELETE',
		});
		const task_json = await cancel_response.json();
	}
	function shortenTaskID(task_id) {
		return task_id.slice(0, 5) + "...";
	}
</script>
<style>
.cmresult {
	border-style: solid;
}
</style>
<div class="cmresult">
{#if !task_status}
Creating the task...
{:else}
<dl>
	<dt>task_id</dt><dd>{shortenTaskID(task.task_id)}</dd>
	<dt>status</dt><dd>{task_status.status}</dd>
	results: {JSON.stringify(task_status.result)}
</dl>
<button on:click|once={cancel} disabled={!is_task_pending}>Cancel task</button>
{/if}
</div>
