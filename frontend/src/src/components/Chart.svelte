<script>
    import {afterUpdate} from 'svelte';

    export let data;
    export let labels;
    export let task;
    let chart_id;
    let chart;

  $: {
    chart_id = "chart_" + task.id;
  }

  async function createChart() {
      const ctx = document.getElementById(chart_id).getContext('2d');
      const myChart = new Chart(ctx, {
          type: 'bar',
          data: {
              labels,
              datasets: [{
                  label: '# of Votes',
                  data,
                  backgroundColor: [
                      'rgba(255, 99, 132, 0.2)',
                      'rgba(54, 162, 235, 0.2)',
                      'rgba(255, 206, 86, 0.2)',
                      'rgba(75, 192, 192, 0.2)',
                      'rgba(153, 102, 255, 0.2)'
                  ],
                  borderColor: [
                      'rgba(255, 99, 132, 1)',
                      'rgba(54, 162, 235, 1)',
                      'rgba(255, 206, 86, 1)',
                      'rgba(75, 192, 192, 1)',
                      'rgba(153, 102, 255, 1)'
                  ],
                  borderWidth: 1
              }]
          },
          options: {
              scales: {
                  yAxes: [{
                      ticks: {
                          beginAtZero: true
                      }
                  }]
              }
          }
      });
      return myChart;
    }
    afterUpdate(() => {
      if (!chart) {
        chart = createChart();
      }
    });
</script>

<canvas id="{chart_id}"></canvas>
