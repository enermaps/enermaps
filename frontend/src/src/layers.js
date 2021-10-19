// Layers related functions

import {get} from 'svelte/store';
import {layersStore, tasksStore, selectedLayerStore} from './stores.js';
import {getTask, refreshTask, SUCCESS_STATUS} from './tasks.js';
import {getDatasetLayerLegend} from './client.js';


// Create a new layer and put it at the top of the stack, so it is displayed last
export function createLayer(name, labels, title, isRaster, taskId) {
  const layers = get(layersStore);

  let layer = getLayer(name);

  if (layer !== null) {
    layer.effect = 'refresh';
    layer.visible = true;
  } else {
    layer = {
      name: name,
      labels: labels,
      title: title,
      is_raster: isRaster,
      visible: true,
      effect: 'new',
      leaflet_layer: null,
      task_id: taskId,
      legend_promise: (taskId === null ? getDatasetLayerLegend(name) : null),
    };

    layers.unshift(layer);

    if (layers.length == 1) {
      selectedLayerStore.set(layer.name);
    }

    console.log('New layer:', layer);
  }

  layersStore.set(layers);

  return layer;
}


export function recomputeLayer(layer, leafletGroup) {
  const task = getTask(layer.task_id);

  if ((task !== null) && (task.result.status === SUCCESS_STATUS)) {
    refreshTask(task);

    leafletGroup.removeLayer(layer.leaflet_layer);

    layer.effect = 'compute';
    layer.leaflet_layer = null;

    const layers = get(layersStore);
    layersStore.set(layers);
  }
}


// Returns the layer with the given name
export function getLayer(name) {
  const layers = get(layersStore);

  for (const layer of layers) {
    if (layer.name === name) {
      return layer;
    }
  }

  return null;
}


// Delete a layer (and its associated task if necessary)
export function deleteLayer(layer) {
  console.log('Remove layer:', layer.name);

  // Remove the associated task if necessary
  if (layer.task_id !== null) {
    const task = getTask(layer.task_id);
    if (task.hidden) {
      console.log('Remove associated task:', layer.task_id);
      const tasks = get(tasksStore);
      const taskIndex = tasks.indexOf(task);
      tasks.splice(taskIndex, 1);
      tasksStore.set(tasks);
    }
  }

  const layers = get(layersStore);
  const layerIndex = layers.indexOf(layer);
  layers.splice(layerIndex, 1);
  layersStore.set(layers);

  if (get(selectedLayerStore) === layer.name) {
    selectedLayerStore.set(null);
  }
}
