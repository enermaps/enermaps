<script>
  import {onMount} from 'svelte';
  import {BASE_URL} from '../settings.js';
  import {getCMs} from '../client.js';
  import {areaSelectionLayerStore, selectedLayerStore, isCMPaneActiveStore, popupInformation, popupInformationtitle} from '../stores.js';
  import CM from './CM.svelte';
  // import AreaSelection from './AreaSelection.svelte';

  let cms = [];
  let areaSelected = true;
  let layerSelected = true;
  let activeTabTest = 'consultation';


  onMount(async () => {
    cms = await getCMs();
    cms = cms.sort((a, b) => (a.name > b.name) ? 1 : -1);
  });


  $: {
    areaSelected = true;
    if ($areaSelectionLayerStore !== null) {
      const selection = $areaSelectionLayerStore.getSelection();
      areaSelected = (selection != null) && (selection.features.length > 0);
      areaSelected = true;
    }

    layerSelected = ($selectedLayerStore !== null);
    layerSelected = true;
  }

  function closeCMPanel() {
    isCMPaneActiveStore.update((n) => !n);
  }

</script>


<style>

  table {
    font-weight: bold;
  }

  #calculation_modules_content {
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  :global(#hdata) {
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
    max-width: 400px;
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

  input[type='checkbox'] {
    display: none;
  }

  .wrap-collabsible {
    margin: 1.2rem 0;
  }

  .lbl-toggle {
    display: block;
    font-weight: bold;
    font-size: 1.1rem;
    text-transform: uppercase;
    text-align: center;
    padding: 1rem;
    color: #DDD;
    background: #2B338C;
    cursor: pointer;
    border-radius: 0px;
    transition: all 0.25s ease-out;
  }

  .lbl-toggle:hover {
    color: #FFF;
  }

  .lbl-toggle::before {
    content: ' ';
    display: inline-block;
    border-top: 5px solid transparent;
    border-bottom: 5px solid transparent;
    border-left: 5px solid currentColor;
    vertical-align: middle;
    margin-right: .7rem;
    transform: translateY(-2px);
    transition: transform .2s ease-out;
  }

  .toggle:checked+.lbl-toggle::before {
    transform: rotate(90deg) translateX(-3px);
  }

  .collapsible-content {
    max-height: 0px; overflow: hidden;
    transition: max-height .25s ease-in-out;
  }

  .toggle:checked + .lbl-toggle + .collapsible-content {
    max-height: 350px;
  }

  .toggle:checked+.lbl-toggle {
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
  }

  .collapsible-content .content-inner {
    background: rgba(0, 105, 255, .2);
    border-bottom: 1px solid rgba(0, 105, 255, .45);
    border-bottom-left-radius: 7px;
    border-bottom-right-radius: 7px;
    padding: .5rem 1rem;
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
<!--        <AreaSelection />-->
        {#each cms as cm (cm.name)}
          <CM bind:cm />
        {/each}
      {:else if activeTabTest === 'consultation'}
        <div class="popupInformation">
            <div class="wrap-collabsible">
                <input id="collapsible" class="toggle" type="checkbox">
                <label for="collapsible" class="lbl-toggle">{@html $popupInformationtitle}</label>
                    <div class="collapsible-content">
                        <div class="content-inner">
                            <table>
                                {@html $popupInformation}
                            </table>
                        </div>
                    </div>
            </div>

        </div>
      {/if}
    </div>
  </div>
</div>
