<script>
    import { onMount } from 'svelte';
    import Chart from 'chart.js';
    export let datasets;
    let plot_datasets;
    let canvas;
    let chart;

  function getPlotDataset() {
    plot_datasets = []
    for (const key in datasets) {
      const points = datasets[key];
      let plot_points = []
      let index = 0;
      for (const point of points) {
        console.log(point);
        plot_points.push({x: index, y: point})
        index += 1;
        console.log(plot_points);
      }
      plot_datasets.push({label: key, data: plot_points});
    }
    console.log(datasets);
    return plot_datasets;
  }
  async function createChart() {
    const plot_datasets = getPlotDataset()
    console.log(plot_datasets);
    chart = new Chart(canvas, {
      type: 'scatter',
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
