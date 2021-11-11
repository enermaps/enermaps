<script src="../settings.js">
  import {BASE_URL} from '../settings.js';
  import {deleteTask, cancelTask, PENDING_STATUS, REFRESHING_STATUS, FAILURE_STATUS} from '../tasks.js';
  import {tasksStore} from '../stores.js';
  import {recomputeLayer, getLayer} from '../layers.js';
  import {getTaskDownloadLink} from '../client.js';
  import Chart from './Chart.svelte';
  import Value from './Value.svelte';

  export let task;
  export let displayCloseButton = true;

  let displayedTaskId = null;
  let graphs = {};
  let values = [];
  let legend = {};
  const warnings = [];
  let parameters = [];
  let isTaskPending = true;
  let isTaskFailed = false;
  let activeTab = 'result';
  let effectTimer = null;


  function formatTaskID(task) {
    return task.id.slice(0, 5) + '...';
  }


  $: {
    if (isTaskPending || (displayedTaskId !== task.id)) {
      isTaskPending = (task.result.status === PENDING_STATUS) ||
                      (task.result.status === REFRESHING_STATUS);
      isTaskFailed = (task.result.status === FAILURE_STATUS);

      if (!isTaskPending) {
        if (typeof task.result.result === 'string') {
          values.push(['details', task.result.result]);
        } else {
          graphs = task.result.result.graphs;
          values = Object.entries(task.result.result.values);
          legend = task.result.result.legend;

          if (task.result.result.warnings != null) {
            for (const key of Object.keys(task.result.result.warnings)) {
              warnings.push({
                title: key,
                details: task.result.result.warnings[key],
              });
            }
          }
        }

        parameters = Object.entries(task.parameters.parameters);

        displayedTaskId = task.id;
      }
    }

    if ((task.effect !== null) && (effectTimer === null)) {
      effectTimer = window.setTimeout(() => {
        endEffect(task);
      }, 500);
    }
  }

  function endEffect(task) {
    effectTimer = null;
    task.effect = null;
    $tasksStore = $tasksStore;
  }


  async function download() {
    const url = await getTaskDownloadLink(task);

    if (url !== null) {
      window.open(url);
    } else {
      recomputeLayer(getLayer(task.layer), null);
    }
  }
</script>


<style>
  .cmresult {
    padding: 5px;
    background-color: #fff;
    line-height: normal;
  }

  .cmresult.flash {
    background-color: #ff9933;
  }

  .cmresult:not(:last-child) {
    margin-bottom: 5px;
  }

  .container {
    background-color: #fff;
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

  .cmresult.flash div.tabs {
    background-color: #ff9933;
  }

  span.tab {
    border: 1px solid black;
    padding: 4px;
    margin-left: 0;
    margin-right: 0;
    background-color: #f7f7f7;
    cursor: pointer;
  }

  span.tab.selected {
    border-bottom: 1px solid white;
    font-weight: bold;
    background-color: white;
  }

  span.tab.last {
    margin-right: 24px;
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

  span.download {
    position: absolute;
    right: 24px;
    padding-top: 0px;
    cursor: pointer;
  }

  span.download.no-margin {
    right: 8px;
  }

  span.download img {
    width: 12px;
    padding-top: 4px;
  }


  span.close_button {
    position: absolute;
    right: 0;
    padding-top: 0px;
  }

  .box {
    height: 10px;
    width: 10px;
    border: 1px solid black;
    display: inline-block;
  }

  .warning {
    display: block;
    background-color: lightgoldenrodyellow;
    padding: 2px;
    background-image: url(../images/warning_icon.png);
    background-repeat: no-repeat;
    padding-left: 24px;
    background-size: 16px;
    background-position-y: center;
    background-position-x: 4px;
  }

  .warning.first {
    margin-top: 10px;
  }
</style>


<div class="cmresult" class:flash={task.effect === 'flash'}>
  {#if isTaskPending || isTaskFailed }
    <div>
      <span class="close_button" on:click="{() => deleteTask(task)}"><img src='{BASE_URL}images/clear-icon.png' alt='close'></span>
    </div>

    <dl>
      <dt><strong>task_id</strong></dt><dd>{formatTaskID(task)}</dd>
      <dt><strong>status</strong></dt><dd>{task.result.status}</dd>

      {#if isTaskFailed}
        <dt><strong>error</strong></dt><dd>{task.result.result}</dd>
      {/if}
    </dl>

    <button on:click|once={() => cancelTask(task)} hidden={!isTaskPending}>Cancel task</button>
  {:else}
    <div class="container">
      <div class="tabs">
        <span class="tab" class:selected={activeTab === 'parameters'} on:click={() => (activeTab = 'parameters')}>Parameters</span>
        <span class="tab" class:last={!legend} class:selected={activeTab === 'result'} on:click={() => (activeTab = 'result')}>Result</span>
        {#if legend}
          <span class="tab last" class:selected={activeTab === 'legend'} on:click={() => (activeTab = 'legend')}>Legend</span>
        {/if}
        <span class="download" class:no-margin={!displayCloseButton} on:click={() => (download())}>
          <img src='{BASE_URL}images/download-icon.png' alt='download' title="Download the results">
        </span>
        {#if displayCloseButton }
          <span class="close_button" on:click="{deleteTask(task)}">
            <img src='{BASE_URL}images/clear-icon.png' alt='close'>
          </span>
        {/if}
      </div>

      {#if activeTab === 'parameters'}
        <dl>
          {#each parameters as parameter}
            <Value value={parameter}/>
          {/each}
        </dl>

      {:else if activeTab === 'result'}
        <dl>
          {#each values as value}
            <Value value={value}/>
          {/each}
        </dl>

        <Chart datasets={graphs}/>

        {#each warnings as warning, index}
          <div class="warning" class:first={index == 0}><strong>{warning.title}:</strong>&nbsp;{warning.details}</div>
        {/each}

      {:else if activeTab === 'legend'}
        <dl>
          <div class="scroll">
            {#each legend.symbology as symbol}
              <div>
                <div class='box' style="background-color: rgb( {symbol.red}, {symbol.green}, {symbol.blue} )"> </div>
                <div style="display: inline-block;">{symbol.label}</div><br>
              </div>
            {/each}
          </div>
        </dl>
      {/if}
    </div>
  {/if}
</div>
