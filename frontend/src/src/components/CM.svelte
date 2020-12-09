<script>
  import {afterUpdate} from 'svelte';
  import {postCMTask} from '../client.js';
  import CMTask from './CMTask.svelte';
  import {activeOverlayLayersStore, activeSelectionLayerStore} from '../stores.js';
  import 'brutusin-json-forms';
  const BrutusinForms = brutusin['json-forms'];

  export let cm;
  let isDisabled = true;
  let tasks = [];
  let form = undefined;

  afterUpdate(async () =>{
    // was the form already rendered ?
    if (!!form) {
      return;
    }
    const container = document.getElementById('form' + cm.name);
    form = BrutusinForms.create(cm.schema);
    form.render(container);
  });

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

  $ : {
    let isEnabled = $activeOverlayLayersStore.length && $activeSelectionLayerStore !== undefined;
    isDisabled = !isEnabled
  }
</script>
<style>
.tasks {
  overflow: auto;
}
</style>
<div>
  <form id="form{cm.name}">
  </form>
  <button type=submit on:click={() => callCM(cm)} disabled={isDisabled}>{cm.pretty_name}</button>
  <div class="tasks">
  {#each tasks as task}
    <CMTask {cm} {task}/>
  {/each}
  </div>
</div>
