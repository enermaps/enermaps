<script>
  import {onMount} from 'svelte';
  import {getAreas} from '../client.js';
  import {selectionStore} from '../stores.js';


  let availableAreas = null;


  onMount(async () => {
    availableAreas = await getAreas();

    console.log(availableAreas.length + ' areas found');

    availableAreas.push({
      id: 'selection',
      title: 'Selection',
    });
  });


  $: {
    if ($selectionStore !== undefined) {
      console.log('Area selection changed to ' + $selectionStore);
    }
  }
</script>


<style>
  #area_selection {
    width: 240px;
    padding: 4px;
    border: 1px solid #27275b;
    border-radius: 0px;
    background-color: #eff4fa !important;
    box-sizing: border-box;
  }

  #area_selection h3 {
    margin: 0px;
    height: 25px;
    display: flex;
    flex-direction: column;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden !important;
  }

  h3 {
    flex-shrink: 0;
    border : none;
  }

  #areas {
    overflow-y: auto;
    border : none;
  }

  label {
    display: block;
    overflow-y: auto;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow-x: hidden;
    margin-top: 2px;
  }
</style>


<div id="area_selection" on:click|stopPropagation on:dblclick|stopPropagation on:wheel|stopPropagation>
  {#if !availableAreas}
    Loading areas...
  {:else}
    <h3>Area selection</h3>
    <div id="areas">
      {#each availableAreas as area}
        <label title={area.title}>
          <input type=radio bind:group={$selectionStore} value={area.id}>
          {area.title}
        </label>
      {/each}
    </div>
  {/if}
</div>
