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

  let datasetsContainer = null;
  let layersContainer = null;
  let detailsContainer = null;

  let datasetsPanel = null;
  let layersPanel = null;

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
    if (layersContainer === null) {
      return;
    }

    if (detailsContainer == null) {
      await tick();
    }

    await tick();

    const windowHeight = window.innerHeight;

    let rectDatasets = datasetsContainer.getBoundingClientRect();
    let rectLayers = layersContainer.getBoundingClientRect();

    // Attempt to fit everything in one column
    const maxHeight = (windowHeight - (rectDatasets.top - 20)) / 2;

    layersContainer.style.marginTop = 0;
    layersPanel.setMaxHeight(maxHeight);
    rectLayers = layersContainer.getBoundingClientRect();

    const maxHeight2 = windowHeight - rectDatasets.top - 20 - rectLayers.height;
    let oneColumn = true;

    if (maxHeight2 >= Math.max(maxHeight, 300)) {
      datasetsPanel.setMaxHeight(maxHeight2);
      rectDatasets = datasetsContainer.getBoundingClientRect();

      layersContainer.style.left = '10px';
      layersContainer.style.top = (rectDatasets.bottom + 10) + 'px';
      rectLayers = layersContainer.getBoundingClientRect();
    } else {
      const height = windowHeight - rectDatasets.top - 10;

      layersPanel.setMaxHeight(height);
      layersContainer.style.left = (rectDatasets.right + 10) + 'px';
      layersContainer.style.top = rectDatasets.top + 'px';
      rectLayers = layersContainer.getBoundingClientRect();

      datasetsPanel.setMaxHeight(height);
      rectDatasets = datasetsContainer.getBoundingClientRect();

      oneColumn = false;
    }

    // Is there enough room for the details panel?
    if (detailsContainer !== null) {
      const rectDetails = detailsContainer.getBoundingClientRect();

      if (rectDetails.height > windowHeight - (rectLayers.bottom + 20)) {
        detailsContainer.style.left = (rectLayers.right + 10) + 'px';

        if (oneColumn && (rectDetails.height > windowHeight - (rectLayers.top + 10))) {
          detailsContainer.style.top = (windowHeight - rectDetails.height - 10) + 'px';
        } else {
          detailsContainer.style.top = rectLayers.top + 'px';
        }
      } else {
        detailsContainer.style.left = rectLayers.left + 'px';
        detailsContainer.style.top = (rectLayers.bottom + 10) + 'px';
      }
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
    position: fixed;
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
  <div class="datasets" bind:this={datasetsContainer}>
    <DatasetSelection bind:this={datasetsPanel} on:layout={recomputeLayout} />
  </div>
  <div class="layers" bind:this={layersContainer}>
    <Layers bind:this={layersPanel}
            on:selectedLayerVisibilityChanged={onSelectedLayerVisibilityChanged}
            on:layout={recomputeLayout} />
  </div>
</div>

{#if mustDisplayDetails}
  <div class="details" bind:this={detailsContainer} on:mouseover={() => map.dragging.disable()}
       on:mouseout={() => map.dragging.enable()}><Details /></div>
{/if}
