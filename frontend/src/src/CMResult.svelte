<script>
	import { onMount } from 'svelte';
	export let cm_task;
	let cm_status;

	onMount(async() => {
		getTaskResult();
	});
	async function getTaskResult() {
		const task_response = await fetch('/api/cm/' + cm_task.cm.name + '/task/' + cm_task.task_id);
		const task_status = await task_response.json();
		console.log(cm_status);
		cm_status = task_status;
		if (task_status.status === 'PENDING') {
		    setTimeout(getTaskResult, 500)
        }
	}
</script>

task_id: {cm_task.task_id}
task_name: {cm_task.cm.name}
status: {JSON.stringify(cm_status)}
<!--
results: {JSON.stringify(cm_task.result)}
-->
