<script src="../settings.js">
  import {BASE_URL} from '../settings.js';
  import {deleteTask, cancelTask, PENDING_STATUS, REFRESHING_STATUS, FAILURE_STATUS} from '../tasks.js';
  import Chart from './Chart.svelte';
  import Value from './Value.svelte';

  export let task;

  let graphs = {};
  let values = [];
  let parameters = [];
  let isTaskPending = true;
  let isTaskFailed = false;
  let activeTab = 'result';


  function formatTaskID(task) {
    return task.id.slice(0, 5) + '...';
  }


  $: {
    if (isTaskPending) {
      isTaskPending = (task.result.status === PENDING_STATUS) ||
                      (task.result.status === REFRESHING_STATUS);
      isTaskFailed = (task.result.status === FAILURE_STATUS);

      if (!isTaskPending) {
        if (typeof task.result.result === 'string') {
          values.push(['details', task.result.result]);
        } else {
          graphs = task.result.result.graphs;
          values = Object.entries(task.result.result.values);
        }

        parameters = Object.entries(task.parameters.parameters);
      }
    }
  }
</script>


<style>
  .cmresult {
    padding: 5px;
    background-color: #fff;
    background-color: white;
  }

  .cmresult:not(:last-child) {
    margin-bottom: 5px;
  }

  img {
    max-width:100%;
    height:auto;
    cursor: pointer;
  }

  div.tabs {
    border-bottom: 1px solid black;
    margin-top: 5px;
    margin-bottom: 6px;
    padding-bottom: 4px;
  }

  div.tabs span:not(.close_button) {
    border: 1px solid black;
    padding: 4px;
    margin-left: 0;
    margin-right: 0;
    background-color: #f7f7f7;
    cursor: pointer;
  }

  div.tabs span.selected:not(.close_button) {
    border-bottom: 1px solid white;
    font-weight: bold;
    background-color: white;
  }

  dl {
    margin: 0px;
  }

  dd {
    margin-bottom: 5px;
  }

  button {
    margin-top: 10px;
    padding-left: 10px;
    padding-right: 10px;
  }

  span.close_button {
    position: absolute;
    right: 0;
    padding-top: 0px;
  }
</style>


<div class="cmresult">
  {#if isTaskPending || isTaskFailed }
    <div>
      <span class="close_button" on:click="{deleteTask(task)}"><img src='{BASE_URL}images/clear-icon.png' alt='close'></span>
    </div>

    <dl>
      <dt><strong>task_id</strong></dt><dd>{formatTaskID(task)}</dd>
      <dt><strong>status</strong></dt><dd>{task.result.status}</dd>

      {#if isTaskFailed}
        <dt><strong>error</strong></dt><dd>{task.result.result}</dd>
      {/if}
    </dl>
  {:else}
    <div class="tabs">
      <span class:selected={activeTab === 'parameters'} on:click={() => (activeTab = 'parameters')}>Parameters</span>
      <span class:selected={activeTab === 'result'} on:click={() => (activeTab = 'result')}>Result</span>
      <span class="close_button" on:click="{deleteTask(task)}"><img src='{BASE_URL}images/clear-icon.png' alt='close'></span>
    </div>

    {#if activeTab === 'parameters' }
      <dl>
        {#each parameters as parameter}
          <Value value={parameter}/>
        {/each}
      </dl>

    {:else}
      <dl>
        {#each values as value}
          <Value value={value}/>
        {/each}
      </dl>

      <Chart datasets={graphs}/>
    {/if}
  {/if}

  <button on:click|once={cancelTask(task)} hidden={!isTaskPending}>Cancel task</button>
</div>
