import {writable} from 'svelte/store';

export const activeSelectionLayerStore = writable();
export const activeOverlayLayersStore= writable([]);
export const activeCMOutputLayersStore= writable([]);

export const layersStore = writable([]);

export const isCMPaneActiveStore = writable(false);
