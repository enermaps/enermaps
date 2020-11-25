<script>
	import { onMount } from 'svelte';
	export let cm_task;
	let cm_status;

	onMount(async() => {
		getTaskResult();
	});
	async function getTaskResult() {
		const result = await fetch('/api/cm/' + cm_task.cm.name + '/task/' + cm_task.task_id);
		cm_status = await result.json();
		console.log(cm_status);
		cm_status = cm_status;
	}
</script>

task_id: {cm_task.task_id}
task_name: {cm_task.cm.name}
status: {JSON.stringify(cm_status)}
