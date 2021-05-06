<script>
  import {onMount} from 'svelte';
  import Chart from 'chart.js';
  export let datasets;

  let lineDatasets = [];
  let xyDatasets = [];
  const barDatasets = [];

  let xyCanvas;
  let lineCanvas;
  let barCanvas;

  let xyChart;
  let lineChart;

  function processDatasets() {
    for (const [datasetName, dataset] of Object.entries(datasets)) {
      console.log('inserting dataset ' + datasetName);
      insertDataset(datasetName, dataset);
    }
  }

  function insertDataset(name, dataset) {
    const values = dataset.values;
    if (values.length === 0) {
      console.log('empty graph ' + name + ', skip this graph');
      return;
    }
    const graphType = dataset.type;
    switch (graphType) {
      case 'xy':
        insertXYChart(name, dataset);
        break;
      case 'bar':
        insertBarChart(name, dataset);
        break;
      case 'line':
        insertLineChart(name, dataset);
        break;
      default:
    }
  }
  function insertBarChart(name, dataset) {
    // not implemented yet
  }
  function insertLineChart(name, dataset) {
    const chartPoints = [];
    const values = dataset.values;
    for (let x = 0; x < values.length; x++) {
      chartPoints.push({x: x, y: values[x]});
    }
    lineDatasets.push({label: name, data: chartPoints});
    lineDatasets = lineDatasets;
  }

  function insertXYChart(name, dataset) {
    const points = dataset.values;
    const chartPoints = [];
    for (const point of points) {
      chartPoints.push({x: point[0], y: point[1]});
    }
    xyDatasets.push({label: name, data: chartPoints});
    xyDatasets = xyDatasets;
  }

  async function createChart() {
    processDatasets(datasets);
    if (xyDatasets.length) {
      xyChart = new Chart(xyCanvas, {
        type: 'scatter',
        data: {
          datasets: xyDatasets,
        },
      });
    } else {
      xyCanvas.hidden = true;
    }
    if (lineDatasets.length) {
      lineChart = new Chart(lineCanvas, {
        type: 'scatter',
        data: {
          datasets: lineDatasets,
        },
      });
    } else {
      lineCanvas.hidden = true;
    }
    if (barDatasets.length) {
      lineChart = new Chart(barCanvas, {
        type: 'bar',
        data: {
          datasets: barDatasets,
        },
      });
    } else {
      barCanvas.hidden = true;
    }
  }

  onMount(createChart);
</script>
<style>
.graph {
  max-width: 300px;
}
</style>
<div class="graph-container">
  <canvas class="graph" bind:this={xyCanvas}/>
  <canvas class="graph" bind:this={barCanvas}/>
  <canvas class="graph" bind:this={lineCanvas}/>
</div>
