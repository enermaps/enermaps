<script>
  import {onMount, createEventDispatcher, afterUpdate} from 'svelte';
  import {getDatasetsWithVariables, getDatasetLayerName} from '../client.js';
  import {createLayer} from '../layers.js';


  let availableDatasets = null;
  let filter = '';
  let filteredDatasets = [];
  const topics = [];
  let selectedTopic = null;

  let rootElement = null;
  let datasetsContainer = null;
  let disableLayoutEvent = false;

  const dispatch = createEventDispatcher();


  onMount(async () => {
    const datasets = await getDatasetsWithVariables();

    for (const dataset of datasets) {
      dataset.open = false;

      dataset.info.both = false;
      dataset.info.variables_only = false;
      dataset.info.time_period_only = false;
      dataset.info.unique = false;
      dataset.info.const_variable = null;
      dataset.info.const_time_period = null;
      dataset.info.open_intermediate_layers = [];

      if ((dataset.info.variables.length > 1) && (dataset.info.time_periods.length > 1)) {
        dataset.info.both = true;
      } else if ((dataset.info.variables.length > 1) &&
                 (dataset.info.time_periods.length == 1)) {
        dataset.info.variables_only = true;
        dataset.info.const_time_period = dataset.info.time_periods[0];
      } else if ((dataset.info.variables.length > 1) &&
                 (dataset.info.time_periods.length == 0)) {
        dataset.info.variables_only = true;
      } else if ((dataset.info.variables.length == 1) &&
                 (dataset.info.time_periods.length > 1)) {
        dataset.info.time_period_only = true;
        dataset.info.const_variable = dataset.info.variables[0];
      } else if ((dataset.info.variables.length == 0) &&
                 (dataset.info.time_periods.length > 1)) {
        dataset.info.time_period_only = true;
      } else {
        dataset.info.unique = true;

        if (dataset.info.variables.length == 1) {
          dataset.info.const_variable = dataset.info.variables[0];
        }

        if (dataset.info.time_periods.length == 1) {
          dataset.info.const_time_period = dataset.info.time_periods[0];
        }
      }

      if ((dataset.group != '') && (topics.indexOf(dataset.group) == -1)) {
        topics.push(dataset.group);
      }
    }

    datasets.sort(function(dataset1, dataset2) {
      const title1 = dataset1.title;
      const title2 = dataset2.title;
      if (title1 < title2) {
        return -1;
      }
      if (title1 > title2) {
        return 1;
      }
      return 0;
    });

    topics.sort();

    console.log(datasets.length + ' datasets found, in ' + topics.length + ' topics');

    availableDatasets = datasets;

    // Allow to display a dataset at launch
    let startDataset = null;

    const urlParams = new URLSearchParams(window.location.search);

    if (urlParams.has('shared_id')) {
      const sharedId = urlParams.get('shared_id');
      for (const dataset of datasets) {
        if (dataset.shared_id == sharedId) {
          startDataset = dataset;
          break;
        }
      }
    } else if (urlParams.has('dataset_id')) {
      const datasetId = parseInt(urlParams.get('dataset_id'));
      for (const dataset of datasets) {
        if (dataset.ds_id == datasetId) {
          startDataset = dataset;
          break;
        }
      }
    }

    if (startDataset !== null) {
      let startVariable = null;
      let startTimePeriod = null;

      if (startDataset.info.default_parameters.variable !== undefined) {
        startVariable = startDataset.info.default_parameters.variable;
      } else if (startDataset.info.variables.length > 0) {
        startVariable = startDataset.info.variables[0];
      }

      if (startDataset.info.time_periods.length > 0) {
        startTimePeriod = startDataset.info.time_periods[0];
      }

      addLayer(startDataset.ds_id, startVariable, startTimePeriod);
    }
  });


  afterUpdate(() => {
    if (!disableLayoutEvent) {
      dispatch('layout', '');
    }

    disableLayoutEvent = false;
  });


  $: {
    if (availableDatasets !== null) {
      filteredDatasets = Array.from(availableDatasets);

      if (selectedTopic !== null) {
        filteredDatasets = filteredDatasets.filter((dataset) =>
          (dataset.group == selectedTopic));
      }

      if (filter != '') {
        filteredDatasets = filteredDatasets.filter((dataset) =>
          dataset.title.toLowerCase().indexOf(filter.toLowerCase()) !== -1);
      }
    }
  }


  async function toggleDataset(dataset) {
    dataset.open = !dataset.open;
    availableDatasets = availableDatasets;
  }


  function toggleIntermediateLayer(dataset, variable) {
    const index = dataset.info.open_intermediate_layers.indexOf(variable);

    if (index >= 0) {
      dataset.info.open_intermediate_layers.splice(index);
    } else {
      dataset.info.open_intermediate_layers.push(variable);
    }

    availableDatasets = availableDatasets;
  }


  function isIntermediateLayerOpen(dataset, variable) {
    return (dataset.info.open_intermediate_layers.indexOf(variable) >= 0);
  }


  async function addLayer(datasetId, variable, timePeriod) {
    const dataset = availableDatasets.filter((dataset) => dataset.ds_id == datasetId)[0];

    const layerName = await getDatasetLayerName(
        datasetId, dataset.is_raster, variable, timePeriod,
    );

    const labels = {
      primary: null,
      secondary: null,
      dataset: null,
    };

    let title = null;

    if (variable !== null) {
      labels.primary = variable;
      labels.dataset = dataset.title;

      if (timePeriod !== null) {
        labels.secondary = timePeriod;
        title = variable + '\n\n' + timePeriod + '\n\n' + dataset.title;
      } else {
        title = variable + '\n\n' + dataset.title;
      }
    } else if (timePeriod !== null) {
      labels.primary = timePeriod;
      labels.dataset = dataset.title;
      title = timePeriod + '\n\n' + dataset.title;
    } else {
      labels.primary = dataset.title;
      title = dataset.title;
    }

    const layerInfos = {
      dataset: dataset.ds_id,
      variable: variable,
    };

    createLayer(
        layerName, labels, title, dataset.is_raster, dataset.is_tiled,
        dataset.info.min_zoom_level, null, layerInfos,
    );
  }


  function isCombinationValid(dataset, variable, timePeriod) {
    if (dataset.info.valid_combinations == null) {
      return true;
    }

    return dataset.info.valid_combinations[timePeriod].indexOf(variable) != -1;
  }


  export function setMaxHeight(maxHeight) {
    if (datasetsContainer !== null) {
      const rectPanel = rootElement.getBoundingClientRect();
      const rectDatasets = datasetsContainer.getBoundingClientRect();

      maxHeight = maxHeight - (rectDatasets.top - rectPanel.top) -
                  (rectPanel.bottom - rectDatasets.bottom);

      datasetsContainer.style.maxHeight = maxHeight + 'px';
      disableLayoutEvent = true;
    }
  }
</script>


<style>
  #datasets_selection {
    width: 240px;
    padding: 4px;
    border: 1px solid #27275b;
    border-radius: 0px;
    background-color: #eff4fa;
    box-sizing: border-box;
  }

  h3 {
    margin: 0px;
    height: 25px;
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    border : none;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden !important;
  }

  .search {
    width: 100%;
  }

  .topics {
    width: 100%;
    margin-top: 4px;
    margin-bottom: 4px;
    font-size: 0;
  }

  .topics label {
    display: inline-block;
    width: 40px;
    font-size: 12px;
  }

  .topics select {
    width: calc(100% - 40px);
    font-size: 12px;
  }

  .scroll {
    max-height: max(calc((100vh - 250px) / 2 - 70px), 200px);
    border : none;
    overflow-y: scroll;
    scrollbar-color: #27275b;
    scrollbar-width: thin;
  }

  table {
    border-collapse: collapse;
  }

  span {
    margin: 0;
  }

  tr {
    cursor: pointer;
  }

  tr.layer.final {
    cursor: copy;
  }

  tr:hover {
    background-color: #72aff9;
  }

  td {
    vertical-align: top;
  }

  td.title {
    font-weight: bold;
  }

  tr.layer.intermediate td {
    font-style: italic;
  }

  td.bullet {
    width: 8px;
  }

  tr.open td.arrow span {
    transform: rotate(90deg);
    display: inline-block;
  }

  .help {
    font-style: italic;
    color: rgb(128,128, 128);
  }
</style>


<div id="datasets_selection" bind:this={rootElement} on:click|stopPropagation
     on:dblclick|stopPropagation on:wheel|stopPropagation>
  <h3>Datasets</h3>

  {#if !availableDatasets}
    Loading datasets...
  {:else}
    <input bind:value={filter} class="search" placeholder="Search dataset...">

    {#if topics.length > 0}
      <div class="topics">
        <label for="topic">Group:</label>
        <select name="topic" bind:value={selectedTopic}>
          <option value={null}>All</option>
          {#each topics as topic}
            <option value={topic}>{topic}</option>
          {/each}
        </select>
      </div>
    {/if}

    {#if filteredDatasets.length > 0}
      <div class="scroll" bind:this={datasetsContainer}>
        <table id="datasets">
          <tbody>
            {#each filteredDatasets as dataset (dataset.ds_id)}
              <tr class="dataset" title={dataset.title} on:click={() => toggleDataset(dataset)} class:open={dataset.open}>
                <td class="arrow"><span>►</span></td>
                <td class="title" colspan="3">{dataset.title}</td>
                <td class="openair">
                  <a href={dataset.openaireLink} title="Link to OpenAIRE metadata" target="_blank">&#128279;</a>
                </td>
              </tr>

              {#if dataset.open}
                {#if dataset.info.both}
                  {#each dataset.info.variables as variable}
                    <tr class="layer intermediate" title={variable}
                        on:click={() => toggleIntermediateLayer(dataset, variable)} class:open={isIntermediateLayerOpen(dataset, variable)}>
                      <td></td>
                      <td class="arrow"><span>►</span></td>
                      <td colspan="2">{variable}</td>
                      <td></td>
                    </tr>

                    {#if isIntermediateLayerOpen(dataset, variable)}
                      {#each dataset.info.time_periods as timePeriod}
                        {#if isCombinationValid(dataset, variable, timePeriod)}
                          <tr class="layer final" title={timePeriod}
                              on:click={() => addLayer(dataset.ds_id, variable, timePeriod)}>
                            <td></td>
                            <td class="bullet"></td>
                            <td class="bullet">◦</td>
                            <td>{timePeriod}</td>
                            <td></td>
                          </tr>
                        {/if}
                      {/each}
                    {/if}
                  {/each}
                {:else if dataset.info.variables_only}
                  {#each dataset.info.variables as variable}
                    <tr class="layer final" title={variable}
                        on:click={() => addLayer(dataset.ds_id, variable, dataset.info.const_time_period)}>
                      <td></td>
                      <td class="bullet">◦</td>
                      <td colspan="2">{variable}</td>
                      <td></td>
                    </tr>
                  {/each}
                {:else if dataset.info.time_period_only}
                  {#each dataset.info.time_periods as timePeriod}
                    <tr class="layer final" title={timePeriod}
                        on:click={() => addLayer(dataset.ds_id, dataset.info.const_variable, timePeriod)}>
                      <td></td>
                      <td class="bullet">◦</td>
                      <td colspan="2">{timePeriod}</td>
                      <td></td>
                    </tr>
                  {/each}
                {:else}
                  <tr class="layer final" title={dataset.title}
                      on:click={() => addLayer(
                        dataset.ds_id, dataset.info.const_variable,
                        dataset.info.const_time_period,
                      )}>
                    <td></td>
                    <td class="bullet">◦</td>
                    {#if dataset.info.const_variable !== null}
                      <td colspan="2">{dataset.info.const_variable}</td>
                    {:else if dataset.info.const_time_period !== null}
                      <td colspan="2">{dataset.info.const_time_period}</td>
                    {:else}
                      <td colspan="2">{dataset.title}</td>
                    {/if}
                    <td></td>
                  </tr>
                {/if}
              {/if}
            {/each}
          </tbody>
        </table>
      </div>

    {:else}
      <span class="help">No dataset matching the filter(s) found</span>
    {/if}
  {/if}
</div>
