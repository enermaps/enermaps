<script>
    import {afterUpdate} from 'svelte';
    export let data;
    //export let labels;
    export let task;
    let chart_id;
    let chart;
  $: {
    chart_id = "chart_" + task.id;
  }
  async function createChart() {
      const ctx = document.getElementById(chart_id).getContext('2d');
      var scatterChart = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Scatter Dataset',
                    data: [{
                        x: -10,
                        y: 0
                    }, {
                        x: 0,
                        y: 10
                    }, {
                        x: 10,
                        y: 5
                    }]
                }]
            },
            options: {
                scales: {
                    xAxes: [{
                        type: 'linear',
                        position: 'bottom'
                    }]
                }
            }
        });
      return scatterChart;
    }
    afterUpdate(() => {
      if (!chart) {
        chart = createChart();
      }
    });
</script>

<canvas id="{chart_id}"></canvas>