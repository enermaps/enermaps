<script src="../settings.js">
  import {onMount, createEventDispatcher} from 'svelte';
  import {deleteTaskResult, getTaskResult, WMS_URL} from '../client.js';
  import {activeCMOutputLayersStore} from '../stores.js';
  import Chart from './Chart.svelte';
  import Value from './Value.svelte';

  export let task;
  export let cm;

  let graphs = {};
  let values = [];
  let parameters = [];
  let taskResult = {status: 'PENDING'};
  let isTaskPending = true;
  let isTaskFailed = false;
  let activeTab = 'result';
  let resultsDisplayed = false;
  let layers = [];

  const updateTime = 500;
  const PENDING_STATUS = 'PENDING';
  const FAILURE_STATUS = 'FAILURE';
  const REVOKED_STATUS = 'REVOKED';
  const dispatch = createEventDispatcher();

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
    if (taskResult.status === REVOKED_STATUS) {
      removeTask();
    } else {
      isTaskPending = (taskResult.status === PENDING_STATUS);
      isTaskFailed = (taskResult.status === FAILURE_STATUS);

      if (!isTaskPending) {
        if (typeof taskResult.result === 'string') {
          values.push(['details', taskResult.result]);
        } else {
          graphs = taskResult.result.graphs;
          // TODO here check if values has an unit, if yes merge unit and value
          values = Object.entries(taskResult.result.values);
        }

        parameters = Object.entries(task.parameters.parameters);

        if (!isTaskFailed) {
          showHideResults();
        }
      }
    }
  }

  function showHideResults() {
    let activeLayers = $activeCMOutputLayersStore;

    if (!resultsDisplayed) {
      for (const value of Object.values(taskResult.result.geofiles)) {
        let layerName = value.split('/');
        layerName = layerName[layerName.length-2] + '/' + layerName[layerName.length-1];

        const layer = L.tileLayer.wms(
            WMS_URL,
            {
              transparent: 'true',
              layers: encodeURIComponent(layerName),
              format: 'image/png',
            },
        );

        layers.push(layer);
        activeLayers.push(layer);
      }
    } else {
      for (const layer of layers) {
        activeLayers = activeLayers.filter((item) => item !== layer);
      }

      layers = [];
    }

    $activeCMOutputLayersStore = activeLayers;

    resultsDisplayed = !resultsDisplayed;
  }

  function removeTask() {
    if (resultsDisplayed) {
      showHideResults();
    }

    dispatch('delete', {});
  }
</script>


<style>
  .cmresult {
    border: 1px solid #27275b;
    border-radius: 0px;
    padding: 5px;
    background-color: #fff;
    background-color: white;
    font-size: 0.9em;
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

  div.tabs span {
    border: 1px solid black;
    padding: 4px;
    margin-left: 0;
    margin-right: 0;
    background-color: #f7f7f7;
    cursor: pointer;
  }

  div.tabs span.selected {
    border-bottom: 1px solid white;
    font-weight: bold;
    background-color: white;
  }

  dl {
    margin: 0px;
    font-size: 0.9em;
  }

  dd {
    margin-bottom: 5px;
  }

  button {
    margin-top: 10px;
  }
</style>


<div class="cmresult">
  <div class="close_button" on:click="{removeTask}"><img src='/images/clear-icon.png' alt='close'></div>

  {#if isTaskPending || isTaskFailed }
    <dl>
      <dt><strong>task_id</strong></dt><dd>{formatTaskID(task)}</dd>
      <dt><strong>status</strong></dt><dd>{taskResult.status}</dd>
    </dl>
  {/if}

  {#if !isTaskPending}
    <div class="tabs">
      <span class:selected={activeTab === 'parameters'} on:click={() => (activeTab = 'parameters')}>Parameters</span>
      <span class:selected={activeTab === 'result'} on:click={() => (activeTab = 'result')}>Result</span>
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

  <button on:click|once={cancel} hidden={!isTaskPending}>Cancel task</button>
  <button on:click={showHideResults} hidden={isTaskPending || isTaskFailed}>{#if !resultsDisplayed }Show{:else}Hide{/if}</button>
</div>
