<script>
  import {onMount, createEventDispatcher, afterUpdate} from 'svelte';
  import {datasetsStore, datasetTopicsStore} from '../stores.js';
  import {getDatasetLayerName} from '../client.js';
  import {getDatasets, getDatasetBySharedId, getDataset} from '../datasets.js';
  import {createLayerSimple} from '../layers.js';
  import {BASE_URL} from '../settings.js';


  let filter = '';
  let filteredDatasets = [];
  let selectedTopic = null;

  let rootElement = null;
  let datasetsContainer = null;
  let disableLayoutEvent = false;
  let copyPopup = null;

  const dispatch = createEventDispatcher();


  onMount(async () => {
    await getDatasets();

    // Allow to display a dataset at launch
    let startDataset = null;

    const urlParams = new URLSearchParams(window.location.search);

    if (urlParams.has('shared_id')) {
      startDataset = getDatasetBySharedId(urlParams.get('shared_id'));
    } else if (urlParams.has('dataset_id')) {
      startDataset = getDataset(urlParams.get('dataset_id'));
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

      createLayerSimple(startDataset.ds_id, startVariable, startTimePeriod);
    }
  });


  afterUpdate(() => {
    if (!disableLayoutEvent) {
      dispatch('layout', '');
    }

    disableLayoutEvent = false;
  });


  $: {
    if ($datasetsStore !== null) {
      filteredDatasets = Array.from($datasetsStore);

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
    $datasetsStore = $datasetsStore;
  }


  function toggleIntermediateLayer(dataset, variable) {
    const index = dataset.info.open_intermediate_layers.indexOf(variable);

    if (index >= 0) {
      dataset.info.open_intermediate_layers.splice(index);
    } else {
      dataset.info.open_intermediate_layers.push(variable);
    }

    $datasetsStore = $datasetsStore;
  }


  function isIntermediateLayerOpen(dataset, variable) {
    return (dataset.info.open_intermediate_layers.indexOf(variable) >= 0);
  }


  async function copyGeoJSONUrlToClipboard(datasetId, variable, timePeriod, event) {
    const dataset = $datasetsStore.filter((dataset) => dataset.ds_id == datasetId)[0];

    if (dataset.is_raster) {
      return;
    }

    const layerName = await getDatasetLayerName(
        datasetId, dataset.is_raster, variable, timePeriod,
    );

    // Create new temporary text element containing the value to copy
    const el = document.createElement('textarea');
    el.value = document.URL + 'api/datasets/geojson/' +
               encodeURIComponent(layerName) + '/';

    // Set non-editable to avoid focus and move outside of view
    el.setAttribute('readonly', '');
    el.style.position = 'absolute';
    el.style.left = '-9999px';
    document.body.appendChild(el);

    // Select text inside element
    el.select();

    // Copy text to clipboard
    document.execCommand('copy');

    // Remove temporary element
    document.body.removeChild(el);

    // Show the popup
    const rect = event.target.getBoundingClientRect();

    if (copyPopup === null) {
      copyPopup = document.createElement('div');
      copyPopup.textContent = 'URL copied to the clipboard';
      copyPopup.style.position = 'absolute';
      copyPopup.style.left = (rect.right + 6) + 'px';
      copyPopup.style.top = rect.top + 'px';
      copyPopup.style.backgroundColor = 'lightgoldenrodyellow';
      copyPopup.style.fontSize = '14px';
      copyPopup.style.padding = '4px';
      document.body.appendChild(copyPopup);
    } else {
      copyPopup.style.left = (rect.right + 6) + 'px';
      copyPopup.style.top = rect.top + 'px';
    }
  }


  function hideCopyPopup() {
    if (copyPopup !== null) {
      document.body.removeChild(copyPopup);
      copyPopup = null;
    }
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
    border: 1px solid #293790;
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
    scrollbar-color: #293790;
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

  td.openaire img {
    height: 16px;
    margin-left: 2px;
  }

  td.geojson img {
    height: 16px;
    margin-left: 2px;
    cursor: pointer;
  }

  .help {
    font-style: italic;
    color: rgb(128,128, 128);
  }
</style>


<div id="datasets_selection" bind:this={rootElement} on:click|stopPropagation
     on:dblclick|stopPropagation on:wheel|stopPropagation>
  <h3>Jeux de données</h3>

  {#if !$datasetsStore}
    Loading datasets...
  {:else}
    <input bind:value={filter} class="search" placeholder="Search dataset...">

    {#if $datasetTopicsStore.length > 0}
      <div class="topics">
        <label for="topic">Group:</label>
        <select name="topic" bind:value={selectedTopic}>
          <option value={null}>All</option>
          {#each $datasetTopicsStore as topic}
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
                <td class="openaire">
                  <a href={dataset.openaireLink} title="Link to OpenAIRE metadata and license" target="_blank">
                    <img src='{BASE_URL}images/info-icon.png' alt="infos" />
                  </a>
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
                              on:click={() => createLayerSimple(dataset.ds_id, variable, timePeriod)}>
                            <td></td>
                            <td class="bullet"></td>
                            <td class="bullet">◦</td>
                            <td>{timePeriod}</td>
                            <td class="geojson">
                              {#if !dataset.is_raster}
                                <img src='{BASE_URL}images/copy-icon.png' alt="geojson link"
                                     title="Copy the URL of the GeoJSON file"
                                     on:click|stopPropagation={(event) => copyGeoJSONUrlToClipboard(
                                       dataset.ds_id, variable, timePeriod, event,
                                     )}
                                     on:mouseleave={hideCopyPopup}/>
                              {/if}
                            </td>
                          </tr>
                        {/if}
                      {/each}
                    {/if}
                  {/each}
                {:else if dataset.info.variables_only}
                  {#each dataset.info.variables as variable}
                    <tr class="layer final" title={variable}
                        on:click={() => createLayerSimple(dataset.ds_id, variable, dataset.info.const_time_period)}>
                      <td></td>
                      <td class="bullet">◦</td>
                      <td colspan="2">{variable}</td>
                      <td class="geojson">
                        {#if !dataset.is_raster}
                          <img src='{BASE_URL}images/copy-icon.png' alt="geojson link"
                               title="Copy the URL of the GeoJSON file"
                               on:click|stopPropagation={(event) => copyGeoJSONUrlToClipboard(
                                 dataset.ds_id, variable,
                                 dataset.info.const_time_period, event,
                               )}
                               on:mouseleave={hideCopyPopup}/>
                        {/if}
                      </td>
                    </tr>
                  {/each}
                {:else if dataset.info.time_period_only}
                  {#each dataset.info.time_periods as timePeriod}
                    <tr class="layer final" title={timePeriod}
                        on:click={() => createLayerSimple(dataset.ds_id, dataset.info.const_variable, timePeriod)}>
                      <td></td>
                      <td class="bullet">◦</td>
                      <td colspan="2">{timePeriod}</td>
                      <td class="geojson">
                        {#if !dataset.is_raster}
                          <img src='{BASE_URL}images/copy-icon.png' alt="geojson link"
                               title="Copy the URL of the GeoJSON file"
                               on:click|stopPropagation={(event) => copyGeoJSONUrlToClipboard(
                                 dataset.ds_id, dataset.info.const_variable,
                                 timePeriod, event,
                               )}
                               on:mouseleave={hideCopyPopup}/>
                        {/if}
                      </td>
                    </tr>
                  {/each}
                {:else}
                  <tr class="layer final" title={dataset.title}
                      on:click={() => createLayerSimple(
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
                    <td class="geojson">
                      {#if !dataset.is_raster}
                        <img src='{BASE_URL}images/copy-icon.png' alt="geojson link"
                             title="Copy the URL of the GeoJSON file"
                             on:click|stopPropagation={(event) => copyGeoJSONUrlToClipboard(
                               dataset.ds_id, dataset.info.const_variable,
                               dataset.info.const_time_period, event,
                             )}
                             on:mouseleave={hideCopyPopup}/>
                      {/if}
                    </td>
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
