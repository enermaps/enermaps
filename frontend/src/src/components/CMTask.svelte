<script>
  import {onMount} from 'svelte';
  import {deleteTaskResult, getTaskResult} from '../client.js';

  export let task;
  export let cm;

  let taskResult = {status: 'PENDING'};
  const updateTime = 500;
  const PENDING_STATUS = 'PENDING';
  $: isTaskPending = (taskResult.status === PENDING_STATUS);

  onMount(async () => {
    updateTaskResult();
  });


  async function updateTaskResult() {
    const taskResponse = await getTaskResult(cm, task);
    taskResult = taskResponse;
    if (taskResult.status === PENDING_STATUS) {
      setTimeout(updateTaskResult, updateTime);
    }
  }
  async function cancel() {
    await deleteTaskResult(cm, task);
  }
  function formatTaskID(task) {
    return task.id.slice(0, 5) + '...';
  }
  $: {
    console.log(cm);
    console.log(task);
  }
</script>
<style>
.cmresult {
  border-style: solid;
}
</style>
<div class="cmresult">
<dl>
  <dt>task_id</dt><dd>{formatTaskID(task)}</dd>
  <dt>status</dt><dd>{taskResult.status}</dd>
  {#if !isTaskPending}
  results: {JSON.stringify(taskResult.result)}
  {/if}
</dl>
<button on:click|once={cancel} disabled={!isTaskPending}>Cancel task</button>
</div>
