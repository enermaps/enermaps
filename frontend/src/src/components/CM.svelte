<script>
  import {onMount} from 'svelte';
  import {createTask} from '../tasks.js';
  import CMTask from './CMTask.svelte';
  import {areaSelectionLayerStore, selectedLayerStore, tasksStore} from '../stores.js';
  import 'brutusin-json-forms';


  const BrutusinForms = brutusin['json-forms'];

  export let cm;
  let isDisabled = true;
  let tasks = [];
  let formElement;
  let form = undefined;
  let callCMTooltip = 'brutison is a brutison';
  let isCollapsed = false;


  onMount(() => {
    form = BrutusinForms.create(cm.schema);
    form.render(formElement);
  });


  $: {
    tasks = $tasksStore;

    if ($selectedLayerStore === null) {
      callCMTooltip = 'A layer needs to be selected first';
    } else if ($areaSelectionLayerStore !== null) {
      callCMTooltip = 'An area needs to be selected first';
    } else {
      callCMTooltip = 'Call the CM ' + cm.pretty_name;
    }

    const isEnabled = ($selectedLayerStore != null) &&
                      ($areaSelectionLayerStore != null);

    isDisabled = !isEnabled;
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
    background-color : #4d88c7;
    margin-top: 8px;
    margin-bottom: 8px;
    padding : 8px;
    border-radius: 4px;
    width: inherit;
  }

  h3 {
    margin: 0;
  }
</style>


<div class="cm_container">
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
