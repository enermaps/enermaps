<script>
  import {onMount} from 'svelte';
  import {BASE_URL} from '../settings.js';
  import {getCMs} from '../client.js';

  import {isCMPaneActiveStore} from '../stores.js';
  import CM from './CM.svelte';

  let cms = [];

  onMount(async () => {
    cms = await getCMs();
  });

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
    float: right;
    z-index: 1000;
    position: absolute;
    top: 0;
    right: 0;
    padding: 5px;
    margin: 8px;
    border-radius: 0px;
    border: 1px solid #27275b;
    background-color: #eff4fa;
    width: 30%;
    min-width: 280px;
    max-width: 500px;
    max-height: 90%;
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
    font-size: 20px;
    display: inline-block;
    vertical-align: middle;
  }

  #list {
    max-height: inherit;
  }

  #cm_list_header div {
    display: inline-block;
  }

  #close_button_cm_list {
    display: inline-block;
    height: 25px;
    width: 25px;
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


<div id="calculation_modules_pane" hidden={!$isCMPaneActiveStore}>
  <div id="calculation_modules_content">
    <div id="cm_list_header">
      <div id="close_button_cm_list" on:click={closeCMPanel}><img src='{BASE_URL}images/clear-icon.png' alt='close'></div>
      <div id="header"><h2>Calculation Modules</h2></div>
    </div>
    <div id="list">
      {#each cms as cm}
        <CM bind:cm />
      {/each}
    </div>
  </div>
</div>
