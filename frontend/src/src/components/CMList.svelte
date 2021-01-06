<script>
  import {onMount} from 'svelte';
  import {getCMs} from '../client.js';

  import {isCMPaneActiveStore} from '../stores.js';
  import CM from './CM.svelte';

  let cms = [];

  onMount(async () => {
    cms = await getCMs();
  });
  function toggleCM() {
    isCMPaneActiveStore.update((n) => !n);
  }
</script>
<style>
#calculation_modules {
  float: right;
  z-index: 1000;
  position: absolute;
  top: 0;
  right: 0;
  padding: 5px;
  margin: 20px;
  border-radius: 4px;
  border-style: solid;
  border-color: grey;
  background-color: rgba(255, 255, 255, 0.6);
  display: flex;
  flex-direction: column;
  height: 80%;
  width: 40%
}
[hidden]{
  display: none !important;
}
#header {
  flex-shrink: 0;
}
#list {
  overflow-y: auto;
}
</style>
<div id="calculation_modules" hidden={!$isCMPaneActiveStore}>
  <div class="close_button" on:click|stopPropagation="{toggleCM}"></div>
    <a id="cm_toggle" title="Display CM" on:click|stopPropagation={toggleCM}></a>
  <div id="cm_toggle_container">
    <h2 id="header">Call a calculation module</h2>
    <div id="list">
      {#each cms as cm}
	<CM bind:cm/>
      {/each}
    </div>
  </div>
</div>
