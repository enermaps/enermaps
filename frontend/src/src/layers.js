// Layers related functions

import {get} from 'svelte/store';
import {layersStore, tasksStore, selectedLayerStore} from './stores.js';
import {getTask, refreshTask, SUCCESS_STATUS} from './tasks.js';
import {getDataset} from './datasets.js';
import {getDatasetLayerLegend, getDatasetLayerName} from './client.js';


// Create a new layer and put it at the top of the stack, so it is displayed last
export function createLayer(
    name, labels, title, isRaster, isTiled, minZoomLevel, taskId, layerInfos,
) {
  const layers = get(layersStore);

  let layer = getLayer(name);

  if (layer !== null) {
    layer.effect = 'blink';
    layer.visible = true;
  } else {
    if (minZoomLevel === null) {
      minZoomLevel = 0;
    }

    layer = {
      name: name,
      labels: labels,
      title: title,
      is_raster: isRaster,
      is_tiled: isTiled,
      min_zoom_level: minZoomLevel,
      visible: true,
      effect: 'new',
      leaflet_layer: null,
      task_id: taskId,
      layer_infos: layerInfos,
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


// Less customizable version of 'addLayer()'
export async function createLayerSimple(datasetId, variable, timePeriod) {
  const dataset = getDataset(datasetId);

  const layerName = await getDatasetLayerName(
      datasetId, dataset.is_raster, variable, timePeriod,
  );

  const labels = {
    primary: null,
    secondary: null,
    dataset: null,
  };

  let title = null;

  if (variable !== null) {
    labels.primary = variable;
    labels.dataset = dataset.title;

    if (timePeriod !== null) {
      labels.secondary = timePeriod;
      title = variable + '\n\n' + timePeriod + '\n\n' + dataset.title;
    } else {
      title = variable + '\n\n' + dataset.title;
    }
  } else if (timePeriod !== null) {
    labels.primary = timePeriod;
    labels.dataset = dataset.title;
    title = timePeriod + '\n\n' + dataset.title;
  } else {
    labels.primary = dataset.title;
    title = dataset.title;
  }

  const layerInfos = {
    dataset: dataset.ds_id,
    variable: variable,
  };

  createLayer(
      layerName, labels, title, dataset.is_raster, dataset.is_tiled,
      dataset.info.min_zoom_level, null, layerInfos,
  );
}


export function markLayerAsRefreshing(layer) {
  if ((layer.effect === null) || ((layer.effect != 'new') &&
      (layer.effect != 'compute'))) {
    layer.effect = 'refresh';

    const layers = get(layersStore);
    layersStore.set(layers);
  }
}


export function markLayerAsRefreshed(layer) {
  if (layer.effect == 'compute') {
    const task = getTask(layer.task_id);
    if ((task === null) || (task.result.status !== SUCCESS_STATUS)) {
      return;
    }
  }

  layer.effect = null;

  const layers = get(layersStore);
  layersStore.set(layers);
}


export function recomputeLayer(layer, leafletGroup) {
  const task = getTask(layer.task_id);

  if ((task !== null) && (task.result.status === SUCCESS_STATUS)) {
    refreshTask(task);

    if (leafletGroup != null) {
      leafletGroup.removeLayer(layer.leaflet_layer);
    }

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
