<script>
  import {tick} from 'svelte';
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

  let layersContainer = null;
  let detailsContainer = null;


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
    recomputeLayout();
  }


  async function displayHideDetails(selectedLayerName) {
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


  async function recomputeLayout(event) {
    if ((layersContainer === null) || !mustDisplayDetails) {
      return;
    }

    if (detailsContainer == null) {
      await tick();
    }

    await tick();

    const rectLayers = layersContainer.getBoundingClientRect();
    const rectDetails = detailsContainer.getBoundingClientRect();

    const windowHeight = window.innerHeight;

    if (rectDetails.height > windowHeight - (rectLayers.bottom + 20)) {
      detailsContainer.style.left = (rectLayers.right + 10) + 'px';

      if (rectDetails.height > windowHeight - (rectLayers.top + 10)) {
        detailsContainer.style.top = (windowHeight - rectDetails.height - 10) + 'px';
      } else {
        detailsContainer.style.top = rectLayers.top + 'px';
      }
    } else {
      detailsContainer.style.left = '10px';
      detailsContainer.style.top = (rectLayers.bottom + 10) + 'px';
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
  .selection {
    position: absolute;
    top: 0;
    left: 250px;
    width: 32px;
  }

  .datasets {
    margin-top: 10px;
  }

  .layers {
    margin-top: 10px;
  }

  .details {
    position: fixed;
    width: fit-content;
  }
</style>


<svelte:window on:resize={recomputeLayout}/>

<div id="left_panel" bind:this={rootElement}>
  <div class="area"><AreaSelection on:layout={recomputeLayout} /></div>
  <div class="selection" bind:this={selectionControls}></div>
  <div class="datasets"><DatasetSelection on:layout={recomputeLayout} /></div>
  <div class="layers" bind:this={layersContainer}>
    <Layers on:selectedLayerVisibilityChanged={onSelectedLayerVisibilityChanged}
            on:layout={recomputeLayout} />
  </div>
</div>

{#if mustDisplayDetails}
  <div class="details" bind:this={detailsContainer} on:mouseover={() => map.dragging.disable()}
       on:mouseout={() => map.dragging.enable()}><Details /></div>
{/if}
