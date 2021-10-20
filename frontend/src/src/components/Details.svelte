<script>
  import {selectedLayerStore} from '../stores.js';
  import {getLayer} from '../layers.js';
  import {getTask} from '../tasks.js';
  import CMTask from './CMTask.svelte';

  let layer = null;
  let task = null;

  $: {
    if ($selectedLayerStore !== null) {
      layer = getLayer($selectedLayerStore);

      if (layer.task_id !== null) {
        task = getTask(layer.task_id);
      } else {
        task = null;
      }
    } else {
      layer = null;
      task = null;
    }
  }
</script>


<style>
  #details {
    padding: 4px;
    border: 1px solid #27275b;
    border-radius: 0px;
    background-color: #eff4fa;
    box-sizing: border-box;
    line-height: normal;
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

  .scroll {
    max-height: max(calc((100vh - 250px) / 3 - 50px), 200px);
    overflow-y: scroll;
    scrollbar-color: #27275b;
    scrollbar-width: thin;
    margin-top: 4px;
    padding-right: 10px;
  }

  @media (max-height: 1000px) {
    .scroll {
      max-height: max(calc((100vh - 250px) / 2 - 50px), 200px);
    }
  }

  .box {
    height: 10px;
    width: 10px;
    border: 1px solid black;
    display: inline-block;
  }

  p.dataset {
    font-style: italic;
    margin-bottom: 6px;
    margin-top: 0;
  }
</style>


<div id="details" on:click|stopPropagation on:dblclick|stopPropagation
     on:wheel|stopPropagation >
  {#if layer }
    {#if task}
      <h3>{layer.labels.primary}</h3>
      <p class="dataset">{layer.labels.dataset}</p>
      <CMTask task={task} displayCloseButton={false} />

    {:else if layer.legend_promise !== null }
      <h3>Legend</h3>
      {#await layer.legend_promise}
        <div>...waiting for legend</div>

      {:then legend}
        {#if legend}
          <div class="scroll">
            {#each legend.symbology as symbol}
              <div>
                <div class='box' style="background-color: rgb( {symbol.red}, {symbol.green}, {symbol.blue} )"> </div>
                <div style="display: inline-block;">{symbol.label}</div><br>
              </div>
            {/each}
          </div>
        {:else}
          <div style="color: red">No legend found</div>
        {/if}

      {:catch error}
        <div style="color: red">{error.message}</div>
      {/await}
    {/if}

  {:else}
    <div>...waiting for informations</div>
  {/if}
</div>
