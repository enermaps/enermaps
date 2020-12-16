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
    let barChart;

function processDatasets() {
      for (const datasetName in datasets) {
        console.log('inserting dataset ' + datasetName);
        const dataset = datasets[datasetName];
        insertDataset(datasetName, dataset);
      }
}

function insertDataset(name, dataset) {
      const values = dataset.values;
      if (values.length === 0) {
        console.log('empty graph ' + name + ', skip this graph');
        return;
      }
      console.log(values);
      const firstValue = values[0];
      if (typeof(firstValue) === 'number') {
        insertLineChart(name, dataset);
        return;
      }
      if (!Array.isArray(firstValue)) {
        console.log('values (' + firstValue + ') of graph ' + name + ' is neither a number nor an array');
        return;
      }
      if (firstValue.length !== 2) {
        console.log(name + ' has an invalid first value ');
        return;
      }

      const first_entry = firstValue[0];
      if (typeof(first_entry) === 'number') {
        insertXYChart(name, dataset);
        return;
      }
      if (typeof(first_entry) === 'string') {
        insertBarChart(name, dataset);
        return;
      }
      console.log('validation problem with graph ' + name);
}
function insertBarChart(name, dataset) {
    // not implemented yet
}
function insertLineChart(name, dataset) {
      const chartPoints = [];
      const values = dataset.values;
      for (const x in values) {
        console.log(x);
        chartPoints.push({x: x, y: values[x]});
        console.log(chartPoints);
      }
      lineDatasets.push({label: name, data: chartPoints});
      lineDatasets = lineDatasets;
      console.log('Inserting ' + name + ' as a line plot');
    }

function insertXYChart(name, dataset) {
      const chartDatasets = [];
      const points = dataset.values;
      const chartPoints = [];
      for (const point of points) {
        console.log(point);
        chartPoints.push({x: point[0], y: point[1]});
        console.log(chartPoints);
      }
      xyDatasets.push({label: name, data: chartPoints});
      xyDatasets = xyDatasets;
      console.log('Inserting ' + name + ' as a xy plot');
}

async function createChart() {
      processDatasets(datasets);
      xyChart = new Chart(xyCanvas, {
        type: 'scatter',
        data: {
          datasets: xyDatasets,
        },
      });
      console.log(xyDatasets);
      lineChart = new Chart(lineCanvas, {
        type: 'scatter',
        data: {
          datasets: lineDatasets,
        },
      });
      console.log(lineDatasets);
      lineChart = new Chart(barCanvas, {
        type: 'bar',
        data: {
          datasets: barDatasets,
        },
      });
      console.log(barDatasets);
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
