<script>
  import {onMount} from 'svelte';
  import {postCMTask} from '../client.js';
  import CMTask from './CMTask.svelte';
  import {activeOverlayLayersStore, activeSelectionLayerStore} from '../stores.js';
  import 'brutusin-json-forms';
  const BrutusinForms = brutusin['json-forms'];

  export let cm;
  let isDisabled = true;
  let tasks = [];
  let formElement;
  let form = undefined;
  let callCMTooltip = 'brutison is a brutison';
  let isCollapsed = false;

  async function callCM() {
    const newTaskParams = {};
    newTaskParams['selection'] = $activeSelectionLayerStore.getSelection();
    newTaskParams['layers'] = $activeOverlayLayersStore.map((layer)=>layer.name);
    newTaskParams['parameters'] = form.getData();
    console.log('Creating new task with parameters: ' + newTaskParams);
    const task = await postCMTask(cm, newTaskParams);

    tasks.push(task);
    tasks = tasks;
  }

  onMount(() => {
    form = BrutusinForms.create(cm.schema);
    form.render(formElement);
  });

  $ : {
    if (!$activeOverlayLayersStore.length) {
      callCMTooltip = 'An overlay layer needs to be selected first';
    } else if (!$activeSelectionLayerStore !== undefined) {
      callCMTooltip = 'A selection layer needs to be selected first';
    } else {
      callCMTooltip = 'Call the CM ' + cm.pretty_name;
    }
    const isEnabled = $activeOverlayLayersStore.length &&
                      $activeSelectionLayerStore !== undefined;
    isDisabled = !isEnabled;
  }

  function toggleCollapse() {
    isCollapsed = !isCollapsed;
  }

  function deleteCMTask(taskToDelete) {
    console.log('Deleting task: ' + taskToDelete.id);
    tasks = tasks.filter((task)=> taskToDelete.id != task.id);
  }
</script>

<style>
.tasks {
  margin-top: 10;
  position: relative;
}

.open_menu {
  display: inline-block;
  height: 25px;
  width: 25px;
  background: url('/images/menu-close-icon.png');
  background-size : 100%;
}

.close_menu {
  display: inline-block;
  height: 25px;
  width: 25px;
  background: url('/images/menu-open-icon.png');
  background-size : 100%;
}

.cm_run {
  vertical-align: middle;
  display: inline-block;
}

.cm_params {
  margin-top: 10px;
  vertical-align: middle;
  display: inline-block;
}

.cm_container {
  background-color : #4d88c7;
  margin-top: 8px;
  margin-bottom: 8px;
  padding : 8px;
  border-radius: 4px;
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
        <button class="cm_run"  type=submit on:click={() => callCM(cm)} disabled={isDisabled} title={callCMTooltip}>Run CM</button>
      </div>
    </div>
  </div>
 
  <div hidden="{isCollapsed}">
    <div>
      <form class="cm_params" bind:this={formElement} />
    </div>
    <div class="tasks">
    {#each [...tasks].reverse() as task (task.id)}
      <CMTask {cm} {task}  on:delete="{() => deleteCMTask(task)}"/>
    {/each}
    </div>
  </div>
</div>