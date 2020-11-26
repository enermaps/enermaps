<script>
	import { onMount } from 'svelte';
	export let cm_task;
	let task_status;
	let is_task_pending = true;

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
		const task_response = await fetch('/api/cm/' + cm_task.cm.name + '/task/' + cm_task.task_id);
		const task_json= await task_response.json();
		task_status = task_json;
		if (task_status.status === 'PENDING') {
		    setTimeout(getTaskResult, 500);
		} else {
			is_task_pending = false;
		}
	}
	async function cancel() {
		const cancel_response = await fetch('/api/cm/' + cm_task.cm.name + '/task/' + cm_task.task_id, {
			method: 'DELETE',
		});
		const task_json = await cancel_response.json();
	}
</script>

task_id: {cm_task.task_id}
task_name: {cm_task.cm.name}
status: {JSON.stringify(task_status)}
<button on:click|once={cancel} disabled={!is_task_pending}>Cancel task</button>
