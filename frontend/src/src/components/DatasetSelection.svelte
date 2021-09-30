<script>
  import {onMount} from 'svelte';
  import {getDatasets, getDatasetVariables} from '../client.js';
  import {layersStore} from '../stores.js';


  let availableDatasets = null;
  let filter = '';
  let filteredDatasets = [];


  onMount(async () => {
    const datasets = await getDatasets();

    for (const dataset of datasets) {
      dataset.open = false;
      dataset.info = null;
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

    console.log(datasets.length + ' datasets found');

    availableDatasets = datasets;
  });


  $: {
    if (availableDatasets !== null) {
      filteredDatasets = availableDatasets.filter((dataset) =>
        dataset.title.toLowerCase().indexOf(filter.toLowerCase()) !== -1);
    }
  }


  async function toggleDataset(dataset) {
    dataset.open = !dataset.open;
    availableDatasets = availableDatasets;

    if (dataset.info === null) {
      dataset.info = await getDatasetVariables(dataset.ds_id);
      availableDatasets = availableDatasets;
    }
  }


  function addLayer(datasetId, variable) {
    const dataset = availableDatasets.filter((dataset) => dataset.ds_id == datasetId)[0];

    const layer = {
      ds_id: datasetId,
      variable: variable,
      title: (variable !== null) ? variable + ', ' + dataset.title : dataset.title,
      is_raster: dataset.is_raster,
      visible: true,
      leaflet_layer: null,
    };

    console.log('New layer:', layer);

    const layers = $layersStore;
    layers.unshift(layer);
    $layersStore = layers;
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

  .scroll {
    max-height: 300px;
    overflow-y: auto;
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

  tr:hover {
    background-color: #72aff9;
  }

  td {
    vertical-align: top;
  }

  td.title {
    font-weight: bold;
  }

  tr.open td.arrow span {
    transform: rotate(90deg);
    display: inline-block;
  }
</style>


<div id="datasets_selection" on:click|stopPropagation on:dblclick|stopPropagation on:wheel|stopPropagation>
  <h3>Datasets</h3>

  {#if !availableDatasets}
    Loading datasets...
  {:else}
    <input bind:value={filter} class="search" placeholder="Search dataset...">

    <div class="scroll">
      <table id="datasets" style="margin-top: 6px;">
        <tbody>
          {#each filteredDatasets as dataset (dataset.ds_id)}
            <tr class="dataset" title={dataset.title} on:click={toggleDataset(dataset)} class:open={dataset.open}>
              <td class="arrow"><span>►</span></td>
              <td class="title" colspan="2">{dataset.title}</td>
              <td class="openair">
                <a href={dataset.openairLink} title="Link to OpenAIRE metadata" target="_blank">&#128279;</a>
              </td>
            </tr>

            {#if dataset.open && dataset.info}
              {#if dataset.info.variables.length > 0}
                {#each dataset.info.variables as variable}
                  <tr class="layer" title={variable} on:click={addLayer(dataset.ds_id, variable)}>
                    <td></td>
                    <td>◦</td>
                    <td>{variable}</td>
                    <td></td>
                  </tr>
                {/each}
              {:else}
                <tr class="layer" title={dataset.title} on:click={addLayer(dataset.ds_id, null)}>
                  <td></td>
                  <td>◦</td>
                  <td>{dataset.title}</td>
                  <td></td>
                </tr>
              {/if}
            {/if}
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</div>
