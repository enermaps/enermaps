<script>
  import {onMount} from 'svelte';
  import {BASE_URL} from '../settings.js';
  import {getCMs} from '../client.js';
  import {areaSelectionLayerStore, selectedLayerStore, isCMPaneActiveStore} from '../stores.js';
  import CM from './CM.svelte';
  import AreaSelection from './AreaSelection.svelte';
//import PopupContent from '../leaflet_components/L.TileLayer.QueryableLayer.js';
//import '../leaflet_components/L.TileLayer.QueryableLayer.css';


  let cms = [];
  let areaSelected = false;
  let layerSelected = false;
  let activeTabTest = 'consultation';


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
    border: 1px solid #2B338C;
    background-color: #eff4fa;
    width: 35vw;
    min-width: 280px;
    max-width: 700px;
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

  div.tabs {
    border-bottom: 1px solid black;
    margin-top: 5px;
    margin-bottom: 6px;
    padding-bottom: 4px;
  }

  span.tab {
    border: 1px solid black;
    padding: 4px;
    margin-left: 0;
    margin-right: 0;
    background-color: #f7f7f7;
    cursor: pointer;
  }

</style>


<div id="calculation_modules_pane" hidden={!$isCMPaneActiveStore}
     on:click|stopPropagation on:dblclick|stopPropagation on:wheel|stopPropagation>

  <div id="calculation_modules_content">
    <div id="cm_list_header">
      <div id="close_button_cm_list" on:click={closeCMPanel}><img src='{BASE_URL}images/clear-icon.png' alt='close'></div>
      <div id="header"><h2>Outils d'analyse : </h2></div>

      {#if !areaSelected}
        <div class="warning">No area selected</div>
      {/if}

      {#if !layerSelected}
        <div class="warning">No layer selected</div>
      {/if}

    </div>
    <div id="list">
      <div class="container-empty-cm">
        <div class="tabs">
          <span class="tab" class:selected={activeTabTest === 'consultation'} on:click={() => (activeTabTest = 'consultation')}>Consultation</span>
          <span class="tab" class:selected={activeTabTest === 'analyse'} on:click={() => (activeTabTest = 'analyse')}>Analyse</span>
        </div>
      </div>
      {#if activeTabTest === 'analyse'}
        <AreaSelection />
        {#each cms as cm (cm.name)}
          <CM bind:cm />
        {/each}
      {:else if activeTabTest === 'consultation'}
        <p> Information about the house. </p>
      {/if}
    </div>
  </div>
</div>
