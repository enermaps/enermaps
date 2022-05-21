<script>
  import {onMount} from 'svelte';
  import {createTask} from '../tasks.js';
  import {createLayerSimple, getLayer} from '../layers.js';
  import CMTask from './CMTask.svelte';
  import {areaSelectionLayerStore, selectedLayerStore, tasksStore, datasetsStore} from '../stores.js';
  import {getDataset} from '../datasets.js';
  import 'brutusin-json-forms';


  const BrutusinForms = brutusin['json-forms'];

  export let cm;
  let isDisabled = true;
  let tasks = [];
  let formElement = null;
  let form = undefined;
  let callCMTooltip = '';
  let isCollapsed = false;
  let layersText = null;
  let layersLinkText = null;
  let layersLinkDatasetId = null;
  let layersDetails = null;
  let layersDetailsDisplayed = false;
  const showCmInfo = false;


  onMount(() => {
    form = BrutusinForms.create(cm.schema);
    form.render(formElement);
  });


  $: {
    tasks = $tasksStore;

    let areaSelected = false;
    if ($areaSelectionLayerStore !== null) {
      const selection = $areaSelectionLayerStore.getSelection();
      areaSelected = (selection != null) && (selection.features.length > 0);
    }

    if ($selectedLayerStore === null) {
      callCMTooltip = 'A layer needs to be selected';
    } else if (!areaSelected) {
      callCMTooltip = 'An area needs to be selected';
    } else {
      callCMTooltip = 'Call the CM ' + cm.pretty_name;
    }

    // Determine if the CM is enabled given the current area/layer selection
    let isEnabled = false;

    if (areaSelected) {
      for (const entry of cm.input_layers) {
        if (entry.dataset === 'none') {
          isEnabled = true;
          callCMTooltip = 'Call the CM ' + cm.pretty_name;
          break;
        }
      }

      if (!isEnabled && ($selectedLayerStore != null)) {
        const layer = getLayer($selectedLayerStore);

        if (layer.layer_infos != null) {
          for (const entry of cm.input_layers) {
            if (entry.dataset === 'all') {
              isEnabled = true;
              break;
            }

            if (((entry.dataset === 'all_rasters') && layer.is_raster) ||
                ((entry.dataset === 'all_vectors') && !layer.is_raster)) {
              isEnabled = true;
              break;
            }

            if (entry.dataset === layer.layer_infos.dataset) {
              if ((layer.layer_infos.variable === null) ||
                  (entry.variables === undefined) ||
                  (entry.variables.length == 0)) {
                isEnabled = true;
                break;
              }

              if (entry.variables.indexOf(layer.layer_infos.variable) >= 0) {
                isEnabled = true;
                break;
              }
            }
          }
        }

        if (!isEnabled) {
          callCMTooltip = 'The selected layer is not usable by this CM';
        }
      }
    }

    isDisabled = !isEnabled;

    // Update the form elements
    if (formElement != null) {
      const inputs = formElement.getElementsByTagName('input');
      for (let i = 0; i < inputs.length; i++) {
        inputs[i].disabled = (isDisabled ? 'disabled' : undefined);
      }

      const selects = formElement.getElementsByTagName('select');
      for (let i = 0; i < selects.length; i++) {
        selects[i].disabled = (isDisabled ? 'disabled' : undefined);
      }
    }

    // Determine the requirement text to display for the CM (only once)
    if ((layersText === null) && ($datasetsStore.length > 0)) {
      for (const entry of cm.input_layers) {
        if (entry.dataset === 'none') {
          layersText = 'Doesn\'t require any specific dataset as input';
          break;
        } else if (entry.dataset === 'all') {
          layersText = 'Works on all datasets';
          break;
        } else if (entry.dataset === 'all_rasters') {
          layersText = 'Works on all raster datasets';
          break;
        } else if (entry.dataset === 'all_vectors') {
          layersText = 'Works on all vector datasets';
          break;
        }
      }

      if (layersText === null) {
        layersDetails = [];

        for (const entry of cm.input_layers) {
          const dataset = getDataset(entry.dataset);
          if (dataset === null) {
            continue;
          }

          layersDetails.push({
            dataset_id: dataset.ds_id,
            dataset_title: dataset.title,
            variables: entry.variables,
          });
        }

        if (layersDetails.length > 1) {
          layersText = 'Works on';
          layersLinkText = layersDetails.length + ' datasets';
        } else {
          const dataset = getDataset(cm.input_layers[0].dataset);
          if (dataset !== null) {
            layersText = 'Works only on the';
            layersLinkText = dataset.title + ' dataset';
            layersLinkDatasetId = dataset.ds_id;
          }
        }
      }
    }
  }


  function toggleCollapse() {
    isCollapsed = !isCollapsed;
  }


  function toggleLayersDetails() {
    layersDetailsDisplayed = !layersDetailsDisplayed;
  }


  async function onDatasetClicked(datasetId, variable) {
    const dataset = getDataset(datasetId);

    let timePeriod = null;

    if (variable == null) {
      if (dataset.info.default_parameters.variable !== undefined) {
        variable = dataset.info.default_parameters.variable;
      } else if (dataset.info.variables.length > 0) {
        variable = dataset.info.variables[0];
      }
    }

    if (dataset.info.time_periods.length > 0) {
      timePeriod = dataset.info.time_periods[0];
    }

    await createLayerSimple(dataset.ds_id, variable, timePeriod);
  }
</script>


<style>
  .tasks {
    margin-top: 10px;
    position: relative;
  }

  .open_menu {
    display: inline-block;
    height: 25px;
    width: 25px;
    background: url('../images/menu-close-icon.png');
    background-size : 100%;
  }

  .cm_run {
    vertical-align: middle;
    display: inline-block;
  }

  .close_menu {
    display: inline-block;
    height: 25px;
    width: 25px;
    background: url('../images/menu-open-icon.png');
    background-size : 100%;
  }

  .cm_params {
    margin-top: 10px;
    overflow-x: auto;
  }

  .cm_container {
    background-color : #6da8d7;
    margin-top: 8px;
    margin-bottom: 8px;
    padding : 8px;
    border-radius: 4px;
    width: inherit;
  }

  .cm_container.disabled {
    background-color: darkgray;
  }

  .cm_info {
    font-style: italic;
    color: rgb(69, 69, 101);
    margin-top: 4px;
  }

  .cm_info span {
    cursor: pointer;
    color: rgb(0,100,200);
  }

  .cm_wiki {
    font-style: italic;
    color: rgb(69, 69, 101);
    margin-top: 4px;
  }

  .cm_wiki a {
    cursor: pointer;
    color: rgb(0,100,200);
  }

  h3 {
    margin: 0;
  }

  .layers-details {
    position: fixed;
    background-color: lightgray;
    border: 1px solid #333333;
    border-radius: 4px;
    padding: 6px;
    margin-left: 20px;
    z-index: 1000;
  }

  .layers-details p {
    margin-top: 0;
  }

  .layers-details ul {
    margin-bottom: 0;
    padding-left: 20px;
  }
</style>


<div class="cm_container" class:disabled={isDisabled}>
  <div class="cm_header">
    <div>
      <h3 class="cm_run">{cm.pretty_name}</h3>
      <div style="float: right;" class="cm_run">
        <div class="cm_run" style="cursor: pointer;" class:open_menu="{isCollapsed}" class:close_menu="{!isCollapsed}" on:click="{toggleCollapse}"></div>
        <span class="cm_run"></span>
        <button class="cm_run" type=submit on:click={() => createTask(cm, form.getData())} disabled={isDisabled} title={callCMTooltip}>Run CM</button>
      </div>
    </div>
  </div>

  <div hidden="{isCollapsed}">
    {#if layersLinkDatasetId}
      <div class="cm_info">
        {layersText}
        {#if layersLinkText}
          <span title="Add the dataset as a layer"
                on:click={() => onDatasetClicked(layersLinkDatasetId, null)}>
            {layersLinkText}
          </span>
        {/if}
      </div>
    {:else}
      {#if showCmInfo}
        <div class="cm_info">
        {layersText}
        {#if layersLinkText}
          <span title="Display the list of supported datasets" on:click={toggleLayersDetails}>{layersLinkText}</span>
        {/if}
        {#if layersDetailsDisplayed && layersDetails}
          <div class="layers-details" on:click={toggleLayersDetails} on:mouseleave={toggleLayersDetails}>
            <p>This CM requires one of the following datasets:</p>
            <ul>
              {#each layersDetails as details}
                <li>
                  {#if details.variables}
                    {details.dataset_title}
                    <ul>
                    {#each details.variables as variable}
                      <li>
                        <span on:click={() => onDatasetClicked(details.dataset_id, variable)}>{variable}</span>
                      </li>
                    {/each}
                    </ul>
                  {:else}
                    <span on:click={() => onDatasetClicked(details.dataset_id, null)}>{details.dataset_title}</span>
                  {/if}
                </li>
              {/each}
            </ul>
          </div>
        {/if}
      </div>
      {/if}
    {/if}

    <div class="cm_wiki">
      <i>
        Pour plus d'information concernant le projet,
        voir <a href="{cm.wiki}" target="_blank">la page web du projet</a>.
      </i>
    </div>

    <div class="cm_params" bind:this={formElement} />
    <div class="tasks">
      {#each [...tasks].reverse() as task (task.id)}
        {#if (task.cm.name === cm.name) && !task.hidden}
          <CMTask task={task} />
        {/if}
      {/each}
    </div>
  </div>
</div>
