<script>
    import { onMount } from 'svelte';
    import Chart from 'chartjs';
    export let data;
    export let labels;
    let chartElement;
    let chart;

    async function createChart() {
      let ctx = chartElement.getContext('2d')
      let myChart = new Chart(ctx, {
          type: 'scatter',
          data: {
              datasets: [{
              label: 'Raster statistic',
              data: data}]
          },
          options: {
              scales: {
                  xAxes: [{
                  type: 'category',
                  labels: labels
                  }]
              }
          }
      });
      chart = myChart;
      console.log(chart, data, labels);
    }
    onMount(createChart);
</script>

<canvas bind:this={chartElement}></canvas>
