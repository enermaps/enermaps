<script>
  import {selectedLayerStore, isCMPaneActiveStore} from '../stores.js';
  import {getLayer} from '../layers.js';
  import {getTask, flashTask, SUCCESS_STATUS} from '../tasks.js';
  import AreaSelection from './AreaSelection.svelte';
  import DatasetSelection from './DatasetSelection.svelte';
  import Layers from './Layers.svelte';
  import Details from './Details.svelte';


  let mustDisplayDetails = false;
  let selectionControls = null;

  let rootElement = null;
  let mapScrollingDisabled = false;
  let map = null;


  selectedLayerStore.subscribe(displayHideDetails);


  $: {
    // Only executed once, but must wait for all the elements to be in place
    if ((rootElement !== null) && !mapScrollingDisabled && (map !== null)) {
      const children = rootElement.children;
      for (let i = 0; i < children.length; i++) {
        // Disable dragging when user's cursor enters the element
        children[i].addEventListener('mouseover', function() {
          map.dragging.disable();
        });

        // Re-enable dragging when user's cursor leaves the element
        children[i].addEventListener('mouseout', function() {
          map.dragging.enable();
        });

        mapScrollingDisabled = true;
      }
    }
  }


  function onSelectedLayerVisibilityChanged(event) {
    displayHideDetails($selectedLayerStore);
  }


  function displayHideDetails(selectedLayerName) {
    mustDisplayDetails = false;

    if (selectedLayerName === null) {
      return;
    }

    const layer = getLayer(selectedLayerName);
    if (!layer.visible) {
      return;
    }

    if (layer.task_id !== null) {
      const task = getTask(layer.task_id);
      mustDisplayDetails = (task !== null) && (task.result.status == SUCCESS_STATUS) &&
                           (task.hidden || !$isCMPaneActiveStore);

      if (!mustDisplayDetails && (task !== null)) {
        flashTask(task);
      }
    } else {
      mustDisplayDetails = true;
    }
  }


  export function disableMapScrolling(theMap) {
    map = theMap;
  }


  export function addSelectionControls(container) {
    selectionControls.appendChild(container);
  }


  export function removeSelectionControls() {
    selectionControls.textContent = '';
  }
</script>


<style>
  #left_panel {
    display: grid;
    grid-template-columns: [col1] auto [col2] auto [last-col];
    grid-template-rows: [row1] auto [row2] auto [row3] auto [row4] 1fr [last-row];
    gap: 10px;
  }

  .area {
    grid-column: col1 / col2;
    grid-row: row1 / row2;
  }

  .selection {
    grid-column: col2 / col3;
    grid-row: row1 / row2;
    width: 32px;
  }

  .datasets {
    grid-column: col1 / col2;
    grid-row: row2 / row3;
  }

  .layers {
    grid-column: col1 / col2;
    grid-row: row3 / row4;
  }

  .details {
    grid-column: col1 / col2;
    grid-row: row4 / last-row;
  }

  @media (max-height: 1000px) {
    .details {
      grid-column: col2 / last-col;
      grid-row: row3 / row4;
    }
  }
</style>


<div id="left_panel" bind:this={rootElement}>
  <div class="area"><AreaSelection /></div>
  <div class="selection" bind:this={selectionControls}></div>
  <div class="datasets"><DatasetSelection /></div>
  <div class="layers"><Layers on:selectedLayerVisibilityChanged={onSelectedLayerVisibilityChanged}/></div>

  {#if mustDisplayDetails}
    <div class="details"><Details /></div>
  {/if}
</div>
