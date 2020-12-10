<script>
  import {onMount} from 'svelte';
  import {getCMs} from '../client.js';

import { isCMPaneActiveStore } from '../stores.js';
  import CM from './CM.svelte';

  let cms = [];

  onMount(async () => {
    cms = await getCMs();
  });
</script>
<style>
#calculation_modules {
  border-style: groove;
}
</style>
<div id="calculation_modules">
  {#if $isCMPaneActiveStore}
  <h2>Call a calculation module</h2>
  {#each cms as cm}
    <CM bind:cm/>
  {/each}
  {/if}
</div>
