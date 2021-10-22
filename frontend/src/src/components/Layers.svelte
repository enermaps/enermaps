<script>
  import {createEventDispatcher, afterUpdate} from 'svelte';
  import {layersStore, selectedLayerStore} from '../stores.js';
  import {deleteLayer} from '../layers.js';
  import {BASE_URL} from '../settings.js';


  let layers = null;
  let selection = null;
  const effectTimers = {};

  const dispatch = createEventDispatcher();


  $: {
    layers = $layersStore;
    selection = $selectedLayerStore;

    for (const layer of layers) {
      if ((layer.effect !== null) && (layer.effect !== 'compute') &&
          (layer.effect !== 'refresh') && (layer.effect !== 'new') &&
          (effectTimers[layer.name] === undefined)) {
        effectTimers[layer.name] = window.setTimeout(() => {
          endEffect(layer);
        }, 500);
      }
    }
  }


  afterUpdate(() => {
    dispatch('layout', '');
  });


  function endEffect(layer) {
    effectTimers[layer.name] = undefined;
    layer.effect = null;
    $layersStore = layers;
  }


  function handleDragStart(e) {
    /* eslint-disable no-invalid-this */

    this.classList.add('dragged');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', this.dataset.layername);

    const layerElements = document.querySelectorAll('#layers_list .layer');

    [].forEach.call(layerElements, function(element) {
      disablePointerEventsInChildren(element);
    });

    /* eslint-enable no-invalid-this */
  }


  function handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    return false;
  }


  function handleDragEnter(e) {
    /* eslint-disable no-invalid-this */
    this.classList.add('over');
    // eslint-enable no-invalid-this */
  }


  function handleDragLeave(e) {
    /* eslint-disable no-invalid-this */
    this.classList.remove('over');
    /* eslint-enable no-invalid-this */
  }


  function handleDrop(e) {
    e.stopPropagation();

    const srcLayerName = e.dataTransfer.getData('text/plain');
    const dstLayerName = this.dataset.layername; // eslint-disable-line no-invalid-this

    if (dstLayerName != srcLayerName) {
      let indexSrc = null;
      let indexDst = null;

      for (let i = 0; i < layers.length; ++i) {
        const layer = layers[i];

        if ((indexSrc === null) && (layer.name === srcLayerName)) {
          indexSrc = i;
        }

        if ((indexDst === null) && (layer.name === dstLayerName)) {
          indexDst = i;
        }

        if ((indexSrc !== null) && (indexDst !== null)) {
          break;
        }
      }

      const tmp = layers[indexSrc];
      layers[indexSrc] = layers[indexDst];
      layers[indexDst] = tmp;

      $layersStore = layers;
    }

    return false;
  }


  function handleDropOnTarget(e) {
    e.stopPropagation();

    const srcLayerName = e.dataTransfer.getData('text/plain');
    const dstLayerName = this.dataset.layername; // eslint-disable-line no-invalid-this

    if (dstLayerName != srcLayerName) {
      let indexSrc = null;

      for (let i = 0; i < layers.length; ++i) {
        const layer = layers[i];

        if (layer.name === srcLayerName) {
          indexSrc = i;
          break;
        }
      }

      const layerToMove = layers.splice(indexSrc, 1)[0];

      if (dstLayerName === '') {
        layers.unshift(layerToMove);
      } else {
        let indexDst = null;

        for (let i = 0; i < layers.length; ++i) {
          const layer = layers[i];

          if (layer.name === dstLayerName) {
            indexDst = i;
            break;
          }
        }

        layers.splice(indexDst + 1, 0, layerToMove);
      }

      $layersStore = layers;
    }

    return false;
  }


  function handleDragEnd(e) {
    const layerElements = document.querySelectorAll('#layers_list .layer');

    [].forEach.call(layerElements, function(element) {
      element.classList.remove('over');
      element.classList.remove('dragged');
    });

    const targetElements = document.querySelectorAll('#layers_list .target');

    [].forEach.call(targetElements, function(element) {
      element.classList.remove('over');
    });

    const elements = document.querySelectorAll('#layers_list .no-pointer-events');

    [].forEach.call(elements, function(element) {
      element.classList.remove('no-pointer-events');
    });
  }


  function changeVisibility(layer) {
    layer.visible = !layer.visible;
    $layersStore = layers;

    if (layer.name === selection) {
      dispatch('selectedLayerVisibilityChanged', layer.visible);
    }

    dispatch('layout', '');
  }


  function selectLayer(layer) {
    if (layer.name !== selection) {
      selection = layer.name;
    } else {
      selection = null;
    }

    $selectedLayerStore = selection;

    dispatch('layout', '');
  }


  function disablePointerEventsInChildren(node) {
    node.childNodes.forEach((child) => {
      disablePointerEventsInChildren(child);

      if (child.classList !== undefined) {
        child.classList.add('no-pointer-events');
      }
    });
  }
</script>


<style>
  #layers_list {
    width: 240px;
    padding: 4px;
    border: 1px solid #27275b;
    border-radius: 0px;
    background-color: #eff4fa;
    box-sizing: border-box;
  }

  h3 {
    margin: 0px;
    height: 25px;
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    border : none;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden !important;
  }

  .help {
    font-style: italic;
    color: rgb(128,128, 128);
  }

  .scroll {
    max-height: max(calc((100vh - 250px) / 2 - 70px), 200px);
    border : none;
    overflow-y: scroll;
    scrollbar-color: #27275b;
    scrollbar-width: thin;
  }

  .layer {
    display: flex;
    line-height: 1.2;
    padding: 0;
    margin: 0;
    border-radius: 4px;
    user-select: none;
    border: 1px solid hsl(240, 8%, 70%);
    background-color: hsl(240, 8%, 93%);
    cursor: pointer;
  }

  .target {
    height: 4px;
  }

  div :global(.layer.over) {
    border: 2px dashed #000;
  }

  div :global(.target.over) {
    border: 2px dashed #000;
    background-color: hsl(240, 8%, 70%);
  }

  div :global(.layer.dragged) {
    opacity: 0.4;
  }

  div :global(.layer.selected) {
    background-color: #6da8d7;
    border: 2px solid #6da8d7;
  }

  div :global(.layer.new) {
    background-color: #5dd798;
  }

  div :global(.layer.blink) {
    background-color: #5dd798;
  }

  div :global(.layer.refresh) {
    background-color: #ff9933;
  }

  div :global(.layer.compute) {
    background-color: #99ff33;
  }

  :global(.no-pointer-events) {
    pointer-events: none;
  }

  div.handle {
    cursor: move;
    background-color: hsl(240, 8%, 70%);
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }

  div.handle p {
    margin: 0 4px 0 4px;
    line-height: 0.4em;
    font-size: medium;
    color: hsl(240, 8%, 40%);
  }

  div.labels {
    flex-grow: 1;
  }

  div.labels p {
    margin: 4px;
    width: 150px;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
  }

  div.labels p.primary {
    font-weight: bold;
  }

  div.labels p.dataset {
    font-style: italic;
  }

  div.delete_button {
    display: inline-block;
    height: 16px;
    width: 16px;
    background-repeat: no-repeat;
    background-size: cover;
    box-sizing: border-box;
    vertical-align: middle;
  }

  div.delete_button img {
    max-width:100%;
    height:auto;
    cursor: pointer;
  }

  .layer input {
    margin-top: 4px;
  }
</style>


<div id="layers_list" on:click|stopPropagation
     on:dblclick|stopPropagation on:wheel|stopPropagation >
  <h3>Layers</h3>

  {#if layers.length == 0}
    <span class="help">Add some layers from the Dataset panel</span>
  {:else}
    <div class="scroll">
      <div class="target" data-layername=""
           on:dragenter={handleDragEnter}
           on:dragover={handleDragOver} on:dragleave={handleDragLeave}
           on:drop={handleDropOnTarget} on:dragend={handleDragEnd} />

      {#each layers as layer (layer.name)}
        <div class="layer" draggable="true" data-layername={layer.name}
             on:dragstart={handleDragStart} on:dragenter={handleDragEnter}
             on:dragover={handleDragOver} on:dragleave={handleDragLeave}
             on:drop={handleDrop} on:dragend={handleDragEnd}
             on:click={selectLayer(layer)} class:selected={layer.name === selection}
             class:new={layer.effect === 'new'} class:refresh={layer.effect === 'refresh'}
             class:compute={layer.effect === 'compute'} class:blink={layer.effect === 'blink'}
             title="{layer.title}">
          <div class="handle">
            <p>∙</p>
            <p>∙</p>
            <p>∙</p>
          </div>
          <input type="checkbox" checked={layer.visible} on:change={changeVisibility(layer)} on:click|stopPropagation />
          <div class="labels">
            <p class="primary">{layer.labels.primary}</p>
            {#if layer.labels.secondary !== null}
              <p class="secondary">{layer.labels.secondary}</p>
            {/if}
            {#if layer.labels.dataset !== null}
              <p class="dataset">{layer.labels.dataset}</p>
            {/if}
          </div>
          <div class="delete_button">
            <img src="{BASE_URL}images/clear-icon.png" title="Remove the layer"
                 alt="Remove the layer" on:click={deleteLayer(layer)}>
          </div>
        </div>

        <div class="target" data-layername={layer.name}
             on:dragenter={handleDragEnter}
             on:dragover={handleDragOver} on:dragleave={handleDragLeave}
             on:drop={handleDropOnTarget} on:dragend={handleDragEnd} />
      {/each}
    </div>
  {/if}
</div>
