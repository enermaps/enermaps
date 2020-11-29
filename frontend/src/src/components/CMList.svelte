<script>
  import {onMount} from 'svelte';
  import {getCMs} from '../client.js';
  import CM from './CM.svelte';

  export let activeOverlayLayers;
  export let activeSelectionLayer;

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
  Call a calculation module
  {#each cms as cm}
    <CM bind:cm bind:activeSelectionLayer bind:activeOverlayLayers/>
  {/each}
</div>
