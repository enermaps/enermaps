<script>
  import {onMount} from 'svelte';
  import {BASE_URL} from '../settings.js';
  import {getCMs} from '../client.js';
  import {areaSelectionLayerStore, selectedLayerStore, isCMPaneActiveStore} from '../stores.js';
  import CM from './CM.svelte';
  import AreaSelection from './AreaSelection.svelte';


  let cms = [];
  let areaSelected = false;
  let layerSelected = false;


  onMount(async () => {
    cms = await getCMs();
    cms = cms.sort((a, b) => (a.name > b.name) ? 1 : -1);
  });


  $: {
    areaSelected = false;
    if ($areaSelectionLayerStore !== null) {
      const selection = $areaSelectionLayerStore.getSelection();
      areaSelected = (selection != null) && (selection.features.length > 0);
    }

    layerSelected = ($selectedLayerStore !== null);
  }


  function closeCMPanel() {
    isCMPaneActiveStore.update((n) => !n);
  }
</script>


<style>
  #calculation_modules_content {
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  #calculation_modules_pane {
    position: relative;
    top: -10px;
    padding: 5px;
    border-radius: 0px;
    border: 1px solid #293790;
    background-color: #eff4fa;
    width: 30vw;
    min-width: 280px;
    max-width: 500px;
    max-height: calc(100vh - 100px);
    overflow-y: scroll;
  }

  [hidden]{
    display: none !important;
  }

  #header h2 {
    padding-top: 0px;
    padding-bottom: 0px;
    margin: 0px;
    flex-shrink: 0;
    text-align: center;
    display: inline-block;
    vertical-align: middle;
  }

  #list {
    max-height: inherit;
  }

  #cm_list_header div {
    display: inline-block;
  }

  #cm_list_header div.warning {
    display: block;
    background-color: lightgoldenrodyellow;
    padding: 2px;
    background-image: url(../images/warning_icon.png);
    background-repeat: no-repeat;
    padding-left: 24px;
    background-size: 16px;
    background-position-y: center;
    background-position-x: 4px;
  }

  #close_button_cm_list {
    display: inline-block;
    height: 20px;
    width: 20px;
    background-repeat: no-repeat;
    background-size: cover;
    box-sizing: border-box;
    vertical-align: middle;
  }

  img {
    max-width:100%;
    height:auto;
    cursor: pointer;
  }
</style>


<div id="calculation_modules_pane" hidden={!$isCMPaneActiveStore}
     on:click|stopPropagation on:dblclick|stopPropagation on:wheel|stopPropagation>

  <div id="calculation_modules_content">
    <div id="cm_list_header">
      <div id="close_button_cm_list" on:click={closeCMPanel}><img src='{BASE_URL}images/clear-icon.png' alt='close'></div>
      <div id="header"><h2>Calculation Modules</h2></div>

      {#if !areaSelected}
        <div class="warning">No area selected</div>
      {/if}

      {#if !layerSelected}
        <div class="warning">No layer selected</div>
      {/if}

      <AreaSelection />
    </div>
    <div id="list">
      {#each cms as cm (cm.name)}
        <CM bind:cm />
      {/each}
    </div>
  </div>
</div>
