import {BASE_URL} from './settings.js';

export const WMS_URL = BASE_URL + 'api/wms?';


async function fetchJSON(endpoint, defaultValue) {
  const response = await fetch(BASE_URL + endpoint);

  if (!response.ok) {
    return defaultValue;
  }

  return await response.json();
}


async function fetchText(endpoint, defaultValue) {
  const response = await fetch(BASE_URL + endpoint);

  if (!response.ok) {
    return defaultValue;
  }

  return response.text();
}


// Datasets-related endpoints --------------------------------------------------

export async function getAreas() {
  return fetchJSON('api/datasets/areas/', []);
}


export async function getDatasets() {
  return fetchJSON('api/datasets/', []);
}


export async function getDatasetVariables(datasetId) {
  return fetchJSON('api/datasets/' + datasetId + '/variables/', {});
}


export async function getDatasetLayerName(datasetId, raster, variable, timePeriod) {
  const prefix = raster ? 'raster' : 'vector';

  if ((variable != null) && (timePeriod != null)) {
    return fetchText(
        'api/datasets/' + datasetId + '/layer_name/' + prefix + '/' +
        btoa(variable) + '/' + timePeriod + '/',
    );
  } else if (variable != null) {
    return fetchText(
        'api/datasets/' + datasetId + '/layer_name/' + prefix + '/' +
        btoa(variable) + '/',
    );
  } else if (timePeriod != null) {
    return fetchText(
        'api/datasets/' + datasetId + '/layer_name/' + prefix + '/-/' +
        timePeriod + '/',
    );
  } else {
    return fetchText('api/datasets/' + datasetId + '/layer_name/' + prefix + '/');
  }
}


export async function getLayerType(layerId) {
  const response = await fetch(BASE_URL + 'api/geofile/' + layerId + '/type/');
  if (!response.ok) {
    return {};
  }
  const legend = await response.json();
  return legend;
}

export async function getLegend(layerId) {
  const response = await fetch(BASE_URL + 'api/geofile/' + layerId + '/legend/');
  if (!response.ok) {
    return {};
  }
  const legend = await response.json();
  return legend;
}

export async function getOpenairLink(layerId) {
  const response = await fetch(BASE_URL + 'api/geofile/' + layerId + '/openair/');
  if (!response.ok) {
    return {};
  }
  const legend = await response.json();
  return legend;
}


export async function getCMs() {
  const response = await fetch(BASE_URL + 'api/cm/');
  if (!response.ok) {
    return [];
  }
  const cmsResponse = await response.json();
  return cmsResponse.cms;
}


export async function postCMTask(cm, parameters) {
  const response = await fetch(BASE_URL + 'api/cm/' + cm.name + '/task/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(parameters),
  });
  const task = await response.json();
  return {'cm': cm, 'id': task.task_id, 'parameters': parameters};
}

export async function getTaskResult(cm, task) {
  const taskResponse = await fetch(
      BASE_URL + 'api/cm/' + cm.name + '/task/' + task.id + '/',
  );
  return await taskResponse.json();
}

export async function deleteTaskResult(cm, task) {
  const taskResponse = await fetch(
      BASE_URL + 'api/cm/' + cm.name + '/task/' + task.id + '/',
      {
        method: 'DELETE',
      });
  return await taskResponse.json();
}
