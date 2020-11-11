<script>
	export let active_overlay_layers;
	export let active_selection_layer;
	let cms = []
</script>

<div>
	{#each cms as cm}
	{cm}
	{/each}
	{#each active_overlay_layers as cm}
	{cm.name}
	{/each}
	{#if active_selection_layer}
	{active_selection_layer.name}
	{/if}
</div>
