/*
A store is simply an object with a subscribe method that allows
interested parties to be notified whenever the store value changes.
*/

import {writable} from 'svelte/store';

export const activeSelectionLayerStore = writable();
export const activeOverlayLayersStore= writable([]);

export const isCMPaneActiveStore = writable(false);
