import {BASE_URL} from './settings.js';

export const WMS_URL = BASE_URL + 'api/wms?';

export async function getLayerType(layerId) {
  const response = await fetch(BASE_URL + 'api/geofile/' + layerId + '/type');
  if (!response.ok) {
    return {};
  }
  const legend = await response.json();
  console.log(legend);
  return legend;
}

export async function getLegend(layerId) {
  const response = await fetch(BASE_URL + 'api/geofile/' + layerId + '/legend');
  if (!response.ok) {
    return {};
  }
  const legend = await response.json();
  console.log(legend);
  return legend;
}

export async function getOpenairLink(layerId) {
  const response = await fetch(BASE_URL + 'api/geofile/' + layerId + '/openair');
  if (!response.ok) {
    return {};
  }
  const legend = await response.json();
  console.log(legend);
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

export async function getGeofiles() {
  const response = await fetch(BASE_URL + 'api/geofile');
  if (!response.ok) {
    console.log(response);
    return [];
  }
  const layersResponse = await response.json();
  return layersResponse;
}

export async function postCMTask(cm, parameters) {
  const response = await fetch(BASE_URL + 'api/cm/' + cm.name + '/task', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(parameters),
  });
  const task = await response.json();
  return {'cm': cm, 'id': task.task_id};
}

export async function getTaskResult(cm, task) {
  const taskResponse = await fetch(BASE_URL + 'api/cm/' + cm.name + '/task/' + task.id);
  return await taskResponse.json();
}

export async function deleteTaskResult(cm, task) {
  const taskResponse = await fetch(BASE_URL + 'api/cm/' + cm + '/task/' + task.id, {
    method: 'DELETE',
  });
  return await taskResponse.json();
}
