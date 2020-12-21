<script src="../settings.js">
  import {onMount} from 'svelte';
  import {deleteTaskResult, getTaskResult} from '../client.js';
  import Chart from './Chart.svelte';
  export let task;
  export let cm;
  export let graphs = {};
  export let values = [];
  let taskResult = {status: 'PENDING'};

  const updateTime = 500;
  const PENDING_STATUS = 'PENDING';

  $: isTaskPending = (taskResult.status === PENDING_STATUS);
  onMount(async () => {
    updateTaskResult();
  });
  async function updateTaskResult() {
    const taskResponse = await getTaskResult(cm, task);
    // The above reponse can be undefined if it encountered an error,
    // just try again if it has
    if (!taskResponse || taskResponse.status === PENDING_STATUS) {
      setTimeout(updateTaskResult, updateTime);
    }
    if (!!taskResponse) {
      taskResult = taskResponse;
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
    if (!isTaskPending) {
      graphs = taskResult.result.graphs;
      // TODO here check if values has an unit, if yes merge unit and value
      values = Object.entries(taskResult.result.values);
    }
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
          {#each values as [name, value]}
            <dt>{name} </dt>
            <dd>{value}</dd>
          {/each}
          <Chart datasets={graphs}/>
  {/if}
</dl>
<button on:click|once={cancel} disabled={!isTaskPending}>Cancel task</button>
</div>
