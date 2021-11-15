<script>
  import {onMount} from 'svelte';
  import {createTask} from '../tasks.js';
  import {getLayer} from '../layers.js';
  import CMTask from './CMTask.svelte';
  import {areaSelectionLayerStore, selectedLayerStore, tasksStore} from '../stores.js';
  import 'brutusin-json-forms';


  const BrutusinForms = brutusin['json-forms'];

  export let cm;
  let isDisabled = true;
  let tasks = [];
  let formElement = null;
  let form = undefined;
  let callCMTooltip = '';
  let isCollapsed = false;


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

    let isEnabled = false;

    if (areaSelected) {
      for (const entry of cm.input_layers) {
        if (entry.dataset === 'none') {
          isEnabled = true;
          break;
        }
      }

      if (!isEnabled && ($selectedLayerStore != null)) {
        const layer = getLayer($selectedLayerStore);

        if (layer.layer_infos != null) {
          for (const entry of cm.input_layers) {
            if ((entry.dataset === 'all') || (entry.dataset === 'none')) {
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
  }


  function toggleCollapse() {
    isCollapsed = !isCollapsed;
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

  h3 {
    margin: 0;
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
