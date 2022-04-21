<script>
  import {onMount} from 'svelte';
  import {getAreas} from '../client.js';
  import {areaSelectionStore, areaSelectionLayerStore} from '../stores.js';


  let availableAreas = null;
  let areaSelection = null;
  let areaSelected = null;


  onMount(async () => {
    availableAreas = await getAreas();

    console.log(availableAreas.length + ' areas found');

    availableAreas.push({
      id: 'selection',
      title: 'Selection',
    });

    $areaSelectionStore = 'NUTS2';
  });


  $: {
    if ($areaSelectionStore !== areaSelection) {
      console.log('Area selection changed to ' + $areaSelectionStore);
      areaSelection = $areaSelectionStore;
    }

    areaSelected = false;
    if ($areaSelectionLayerStore !== null) {
      const selection = $areaSelectionLayerStore.getSelection();
      areaSelected = (selection != null) && (selection.features.length > 0);
    }
  }


  function clearSelection() {
    $areaSelectionLayerStore.clearSelection();
    areaSelected = false;
  }
</script>


<style>
  #area_selection {
    padding: 4px;
    padding-top: 8px;
  }

  label {
    display: inline;
    margin-right: 4px;
    font-weight: bold;
  }

  button {
    padding: 4px;
    margin-left: 4px;
  }
</style>


<div id="area_selection">
  {#if !availableAreas}
    Loading areas...
  {:else}
    <label for="id">Region selection:</label>

    <select id="areas" class="areas" bind:value={$areaSelectionStore}>
      {#each availableAreas as area}
        <option value={area.id}>{area.title}</option>
      {/each}
    </select>

    {#if areaSelected}
      <button on:click={clearSelection}>Clear</button>
    {/if}
  {/if}
</div>
