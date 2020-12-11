<script>
    import { onMount } from 'svelte';
    import Chart from 'chart.js';
    export let data;
    let canvas;
    let chart;

    async function createChart() {
      const ctx = canvas.getContext("2d");
      chart = new Chart(canvas, {
        type: 'line',
        data: data,
      });
      console.log(chart, data, labels);
    }
    onMount(createChart);
</script>
<div class="graph-container">
<canvas bind:this={canvas}/>
</div>
