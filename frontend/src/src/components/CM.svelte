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
  let collapsed = false;

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
    collapsed = !collapsed;
  }

  function deleteCMTask(taskToDelete) {
    console.log('Deleting task: ' + taskToDelete.id);
    tasks = tasks.filter((task)=> taskToDelete.id != task.id);
  }
</script>
<style>
.tasks {
  position: relative;
}
.open_menu {
  display: inline-block;
  height: 30px;
  width: 30px;
  background: url('/images/menu-close-icon.png');
}
.close_menu {
  display: inline-block;
  height: 30px;
  width: 30px;
  background: url('/images/menu-open-icon.png');
}
.cm_name {
  display: inline-block;
  margin: 0px;
}
</style>
  <div class="cm_header">
    <div class:open_menu="{!collapsed}" class:close_menu="{collapsed}" on:click="{toggleCollapse}"></div>
    <h3 class="cm_name">{cm.pretty_name}<h3>
  </div>
  <div hidden="{!collapsed}">
    <form bind:this={formElement} />
      <button type=submit on:click={() => callCM(cm)} disabled={isDisabled} title={callCMTooltip}>{cm.pretty_name}</button>
    <div class="tasks">
    {#each [...tasks].reverse() as task (task.id)}
      <CMTask {cm} {task}  on:delete="{() => deleteCMTask(task)}"/>
    {/each}
    </div>
</div>
