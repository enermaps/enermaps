<script>
  import {onMount} from 'svelte';
  import {deleteTaskResult, getTaskResult} from '../client.js';

  export let task;
  export let cm;

  const taskResult = {status: 'PENDING'};
  let isCancellable = true;
  const updateTime = 500;

  onMount(async () => {
    updateTaskResult();
  });
  function isTaskPending() {
    return taskResult.status === 'PENDING';
  }
  async function updateTaskResult() {
    const taskResponse = getTaskResult(cm.name, task.id);
    taskResult = taskResponse;
    if (isTaskPending()) {
      setTimeout(getTaskResult, updateTime);
    }
  }
  async function cancel() {
    await deleteTaskResult(cm.name, task.id);
  }
  function shortenTaskID(taskId) {
    return taskId.slice(0, 5) + '...';
  }
  $: {
    isCancellable = isTaskPending();
  }
</script>
<style>
.cmresult {
  border-style: solid;
}
</style>
<div class="cmresult">
<dl>
  <dt>task_id</dt><dd>{shortenTaskID(task.id)}</dd>
  <dt>status</dt><dd>{taskResult.status}</dd>
  results: {JSON.stringify(taskResult.result)}
</dl>
<button on:click|once={cancel} disabled={isCancellable}>Cancel task</button>
</div>
