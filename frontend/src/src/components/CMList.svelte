<script>
  import {onMount} from 'svelte';
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
  width: 30%
}
[hidden]{
  display: none !important;
}

#header {
  padding-top: 0px;
  padding-bottom: 0px;
  margin: 0px;
  flex-shrink: 0;
  text-align: center;
}

#list {
  overflow-y: auto;
}

</style>

<div id="calculation_modules_pane" hidden={!$isCMPaneActiveStore}>
  <div class="close_button" on:click={closeCMPanel}></div>
  <div id="calculation_modules_content">
    <h2 id="header">Calculation Modules</h2>
    <div id="list">
      {#each cms as cm}
        <CM bind:cm/>
      {/each}
    </div>
  </div>
</div>
