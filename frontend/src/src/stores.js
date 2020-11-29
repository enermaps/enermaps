import {writable} from 'svelte/store';

export const activeSelectionLayerStore = writable();
export const activeOverlayLayersStore= writable([]);

export const isCMPaneActiveStore = writable(false);
