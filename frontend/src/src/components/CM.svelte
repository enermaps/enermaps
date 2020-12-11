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
    const isEnabled = $activeOverlayLayersStore.length &&
                      $activeSelectionLayerStore !== undefined;
    isDisabled = !isEnabled;
  }
</script>
<style>
.tasks {
  overflow: auto;
}
</style>
<div>
  <form bind:this={formElement} />
  <button type=submit on:click={() => callCM(cm)} disabled={isDisabled}>{cm.pretty_name}</button>
  <div class="tasks">
  {#each tasks as task}
    <CMTask {cm} {task}/>
  {/each}
  </div>
</div>
