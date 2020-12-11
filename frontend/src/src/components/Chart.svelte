<script>
    import { onMount } from 'svelte';
    import Chart from 'chart.js';
    export let data;
    export let labels;
    let chart_element;
    let chart;

    async function createChart() {
        const myChart = new Chart(chart_element, {
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
    }
    onMount(createChart);
</script>

<canvas bind:this={chart_element}></canvas>