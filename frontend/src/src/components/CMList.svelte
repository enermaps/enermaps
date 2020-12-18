<script>
  import {onMount} from 'svelte';
  import {getCMs} from '../client.js';

import {isCMPaneActiveStore} from '../stores.js';
  import CM from './CM.svelte';

  let cms = [];

  onMount(async () => {
    cms = await getCMs();
  });
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
}
</style>
<div id="calculation_modules" hidden={!$isCMPaneActiveStore}>
  <h2>Call a calculation module</h2>
  {#each cms as cm}
    <CM bind:cm/>
  {/each}
</div>
