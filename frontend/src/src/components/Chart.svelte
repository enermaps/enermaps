<script>
    import { onMount } from 'svelte';
    import Chart from 'chart.js';
    export let datasets;
    let plot_datasets;
    let canvas;
    let chart;

  function getPlotDataset() {
    plot_datasets = []
    console.log(datasets);
    for (const key in datasets) {
      plot_datasets.push({label: key, data: datasets[key]});
    }
    return plot_datasets;
  }
  async function createChart() {
    const plot_datasets = getPlotDataset()
    console.log(plot_datasets);
    chart = new Chart(canvas, {
      type: 'line',
      data: {
        datasets: plot_datasets,
      }
    });
    console.log(chart, plot_datasets);
  }
  onMount(createChart);
</script>
<style>
.graph {
  max-width: 300px;
}
</style>
<div class="graph-container">
<canvas class="graph" bind:this={canvas}/>
</div>
