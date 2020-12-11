<script src="../settings.js">
  import {onMount} from 'svelte';
  import {deleteTaskResult, getTaskResult} from '../client.js';
  import Chart from './Chart.svelte';
  export let task;
  export let cm;
  export let plot_data = {};
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
    if (!isTaskPending){
      plot_data = {"first_plot": Array(200).fill(1).map((x, y) => x + y)};
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
    <dt>data : </dt>
    <dd>{Object.keys(JSON.parse(JSON.stringify(taskResult.result))[0])}</dd>

    <dt>results : </dt>
    <dd>{JSON.stringify(taskResult.result)}</dd>

    <dt>TASK</dt>
    <dd>{task.id}</dd>

    <Chart datasets={plot_data}/>

  {/if}
</dl>
<button on:click|once={cancel} disabled={!isTaskPending}>Cancel task</button>
</div>
