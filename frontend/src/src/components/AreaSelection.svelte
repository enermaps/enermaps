<script>
  import {onMount, createEventDispatcher, afterUpdate} from 'svelte';
  import {getAreas} from '../client.js';
  import {areaSelectionStore} from '../stores.js';


  let availableAreas = null;

  const dispatch = createEventDispatcher();


  onMount(async () => {
    availableAreas = await getAreas();

    console.log(availableAreas.length + ' areas found');

    availableAreas.push({
      id: 'selection',
      title: 'Selection',
    });
  });


  $: {
    if ($areaSelectionStore !== undefined) {
      console.log('Area selection changed to ' + $areaSelectionStore);
    }
  }


  afterUpdate(() => {
    dispatch('layout', '');
  });
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

  .areas {
    width: 100%;
  }
  </style>


<div id="area_selection" on:click|stopPropagation on:dblclick|stopPropagation on:wheel|stopPropagation>
  {#if !availableAreas}
    Loading areas...
  {:else}
    <h3>Area selection</h3>

    <select class="areas" bind:value={$areaSelectionStore}>
      <option value={null}>None</option>
      {#each availableAreas as area}
        <option value={area.id}>{area.title}</option>
      {/each}
    </select>
  {/if}
</div>
