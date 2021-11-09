// CM tasks related functions

import {get} from 'svelte/store';
import {areaSelectionLayerStore, selectedLayerStore, tasksStore, layersStore} from './stores.js';
import {postCMTask, deleteTaskResult, getTaskResult} from './client.js';
import {createLayer, getLayer} from './layers.js';


export const PENDING_STATUS = 'PENDING';
export const SUCCESS_STATUS = 'SUCCESS';
export const FAILURE_STATUS = 'FAILURE';
export const REVOKED_STATUS = 'REVOKED';
export const REFRESHING_STATUS = 'REFRESHING';


// Create a new task
export async function createTask(cm, parameters) {
  const params = {};
  params['selection'] = get(areaSelectionLayerStore).getSelection();
  params['layer'] = get(selectedLayerStore);
  params['parameters'] = parameters;

  console.log(
      '[CM ' + cm.name + '] Creating new task with parameters:',
      params.parameters,
  );

  const task = await postCMTask(cm, params);
  task.cm = cm;
  task.result = {status: PENDING_STATUS};
  task.hidden = false;
  task.replacement_for = null;
  task.effect = null;
  task.layer = null;

  console.log('[CM ' + cm.name + '] Created task: ' + task.id);

  const tasks = get(tasksStore);
  tasks.push(task);
  tasksStore.set(tasks);

  console.log('Active tasks:', tasks.map((x) => x.id));

  _retrieveTaskResult(task);
}


// Refresh an existing task (in case its results aren't available anymore
// through the API)
export async function refreshTask(task) {
  console.log('[CM ' + task.cm.name + '] Refreshing task ' + task.id +
              ' with parameters:', task.parameters.parameters);

  const tasks = get(tasksStore);

  task.result = {status: REFRESHING_STATUS};
  tasksStore.set(tasks);

  const newTask = await postCMTask(task.cm, task.parameters);
  newTask.cm = task.cm;
  newTask.result = {status: REFRESHING_STATUS};
  newTask.hidden = false;
  newTask.replacement_for = task.id;
  newTask.effect = null;
  newTask.layer = task.layer;

  console.log('[CM ' + task.cm.name + '] Created task: ' + newTask.id +
              ' to replace ' + task.id);

  const index = tasks.indexOf(task);
  tasks.splice(index, 1, newTask);

  tasksStore.set(tasks);

  console.log('Active tasks:', tasks.map((x) => x.id));

  _retrieveTaskResult(newTask);
}


// Delete a task
export function deleteTask(task) {
  if ((task.result.status === PENDING_STATUS) ||
      (task.result.status === REFRESHING_STATUS)) {
    cancelTask(task);
  } else {
    _deleteTask(task);
  }
}


// Cancel a task and delete it afterwards
export async function cancelTask(task) {
  console.log('[CM ' + task.cm.name + '] Cancelling task: ' + task.id);

  await deleteTaskResult(task);
  _deleteTask(task);
}


// Retrieve a specific task
export function getTask(id) {
  const tasks = get(tasksStore);

  for (const task of tasks) {
    if (task.id === id) {
      return task;
    }
  }

  return null;
}


// Mark a task as "flashing"
export function flashTask(task) {
  task.effect = 'flash';

  const tasks = get(tasksStore);
  tasksStore.set(tasks);
}


function _deleteTask(task) {
  let tasks = get(tasksStore);

  let mustDelete = (task.layer === null);

  if (!mustDelete) {
    const layer = getLayer(task.layer);
    mustDelete = (layer === null) || (task.result.status !== SUCCESS_STATUS);
  }

  if (mustDelete) {
    console.log('[CM ' + task.cm.name + '] Deleting task: ' + task.id);
    tasks = tasks.filter((t) => t.id != task.id);
  } else {
    task.hidden = true;
  }

  tasksStore.set(tasks);
}


async function _retrieveTaskResult(task) {
  const TIMEOUT_MS = 500;

  const taskResponse = await getTaskResult(task);

  // The above reponse can be undefined if it encountered an error,
  // just try again if it has
  if (!taskResponse || taskResponse.status === PENDING_STATUS) {
    setTimeout(
        () => {
          _retrieveTaskResult(task);
        },
        TIMEOUT_MS,
    );
  }

  if (!!taskResponse) {
    task.result = taskResponse;

    if (task.result.status === REVOKED_STATUS) {
      console.log('[CMTask ' + task.id + '] Revoked');
      _deleteTask(task);
    } else if (task.result.status !== PENDING_STATUS) {
      console.log('[CMTask ' + task.id + '] Got response: ' + task.result.status);

      if (task.result.status === SUCCESS_STATUS) {
        _addLayer(task);
      }
    }

    if (task.result.status !== REVOKED_STATUS) {
      const tasks = get(tasksStore);
      tasksStore.set(tasks);
    }
  }
}


function _addLayer(task) {
  if (Object.keys(task.result.result.geofiles).length > 0) {
    if (task.replacement_for !== null) {
      const previousName = 'cm/' + task.result.cm_name + '/' + task.replacement_for;

      const layer = getLayer(previousName);

      layer.name = 'cm/' + task.result.cm_name + '/' + task.result.task_id;
      layer.task_id = task.id;
      layer.effect = null;

      const layers = get(layersStore);
      layersStore.set(layers);

      if (get(selectedLayerStore) === previousName) {
        selectedLayerStore.set(layer.name);
      }

      task.layer = layer.name;
    } else {
      const labels = {
        primary: task.cm.pretty_name,
        secondary: Object.values(task.parameters.parameters).join(', '),
        dataset: null,
      };

      let title = labels.primary + '\n\n';

      for (const key of Object.keys(task.parameters.parameters)) {
        title += key + ': ' + task.parameters.parameters[key] + '\n';
      }

      const refLayer = getLayer(task.parameters.layer);
      if (refLayer != null) {
        if (refLayer.labels.dataset !== null) {
          labels.dataset = refLayer.labels.dataset;
        } else {
          labels.dataset = refLayer.labels.primary;
        }

        title += '\n' + labels.dataset;
      }

      const layerName = 'cm/' + task.result.cm_name + '/' + task.result.task_id;

      createLayer(layerName, labels, title, true, false, null, task.id, null);

      task.layer = layerName;
    }

    const tasks = get(tasksStore);
    tasksStore.set(tasks);
  }
}
