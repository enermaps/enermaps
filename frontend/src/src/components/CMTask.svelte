<script src="../settings.js">
  import {onMount, createEventDispatcher} from 'svelte';
  import {deleteTaskResult, getTaskResult} from '../client.js';
  import Chart from './Chart.svelte';
  import Value from './Value.svelte';
  export let task;
  export let cm;
  let graphs = {};
  let values = [];
  let taskResult = {status: 'PENDING'};

  const updateTime = 500;
  const PENDING_STATUS = 'PENDING';
  const dispatch = createEventDispatcher();

  $: isTaskPending = (taskResult.status === PENDING_STATUS);
  $: {
    console.log(task);
  }
  
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
  $: isTaskPending = taskResult.status === PENDING_STATUS;
  $: if (!isTaskPending) {
    if (typeof taskResult.result === 'string') {
      values.push(['details', taskResult.result]);
    } else {
      graphs = taskResult.result.graphs;
      // TODO here check if values has an unit, if yes merge unit and value
      values = Object.entries(taskResult.result.values);
    }
  }
  function removeTask() {
    dispatch('delete', {});
  }
</script>

<style>
.cmresult {
  border: 1px solid #27275b;
  border-radius: 4px;
  padding: 8px;
  background-color: white;
}
</style>

<div class="cmresult">
  <div class="close_button" on:click="{removeTask}"></div>
  <dl>
  <dt>task_id</dt><dd>{formatTaskID(task)}</dd>
  <dt>status</dt><dd>{taskResult.status}</dd>
  {#if !isTaskPending}
          {#each values as value}
            <Value value={value}/>
          {/each}
          <Chart datasets={graphs}/>
  {:else }
    taskRunning...
  {/if}
</dl>
<button on:click|once={cancel} disabled={!isTaskPending}>Cancel task</button>
</div>
