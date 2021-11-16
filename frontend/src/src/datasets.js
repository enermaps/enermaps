// CM tasks related functions

import {get} from 'svelte/store';
import {datasetsStore, datasetTopicsStore} from './stores.js';
import {getDatasetsWithVariables} from './client.js';


// Retrieve the datasets from the API
export async function getDatasets() {
  const datasets = await getDatasetsWithVariables();
  const topics = [];

  for (const dataset of datasets) {
    dataset.open = false;

    dataset.info.both = false;
    dataset.info.variables_only = false;
    dataset.info.time_period_only = false;
    dataset.info.unique = false;
    dataset.info.const_variable = null;
    dataset.info.const_time_period = null;
    dataset.info.open_intermediate_layers = [];

    if ((dataset.info.variables.length > 1) && (dataset.info.time_periods.length > 1)) {
      dataset.info.both = true;
    } else if ((dataset.info.variables.length > 1) &&
               (dataset.info.time_periods.length == 1)) {
      dataset.info.variables_only = true;
      dataset.info.const_time_period = dataset.info.time_periods[0];
    } else if ((dataset.info.variables.length > 1) &&
               (dataset.info.time_periods.length == 0)) {
      dataset.info.variables_only = true;
    } else if ((dataset.info.variables.length == 1) &&
               (dataset.info.time_periods.length > 1)) {
      dataset.info.time_period_only = true;
      dataset.info.const_variable = dataset.info.variables[0];
    } else if ((dataset.info.variables.length == 0) &&
               (dataset.info.time_periods.length > 1)) {
      dataset.info.time_period_only = true;
    } else {
      dataset.info.unique = true;

      if (dataset.info.variables.length == 1) {
        dataset.info.const_variable = dataset.info.variables[0];
      }

      if (dataset.info.time_periods.length == 1) {
        dataset.info.const_time_period = dataset.info.time_periods[0];
      }
    }

    if ((dataset.group != '') && (topics.indexOf(dataset.group) == -1)) {
      topics.push(dataset.group);
    }
  }

  datasets.sort(function(dataset1, dataset2) {
    const title1 = dataset1.title;
    const title2 = dataset2.title;
    if (title1 < title2) {
      return -1;
    }
    if (title1 > title2) {
      return 1;
    }
    return 0;
  });

  topics.sort();

  console.log(datasets.length + ' datasets found, in ' + topics.length + ' topics');

  datasetsStore.set(datasets);
  datasetTopicsStore.set(topics);
}


export function getDataset(datasetId) {
  const datasets = get(datasetsStore);

  for (const dataset of datasets) {
    if (dataset.ds_id == datasetId) {
      return dataset;
    }
  }

  return null;
}


export function getDatasetBySharedId(sharedId) {
  const datasets = get(datasetsStore);

  for (const dataset of datasets) {
    if (dataset.shared_id == sharedId) {
      return dataset;
    }
  }

  return null;
}
