<script src="../settings.js">
  import {onMount} from 'svelte';
  import {deleteTaskResult, getTaskResult} from '../client.js';
  import Chart from './Chart.svelte';
  export let plot_data = [];
  export let labels = [];
  export let task;
  export let cm;
  let chartid;
  let data_graph;
  let scatterData;
  let taskResult = {status: 'PENDING'};
  const updateTime = 500;
  const PENDING_STATUS = 'PENDING';
  $: isTaskPending = (taskResult.status === PENDING_STATUS);
  onMount(async () => {
    updateTaskResult();
  });
  async function updateTaskResult() {
    const taskResponse = await getTaskResult(cm, task);
    taskResult = taskResponse;
    if (taskResult.status === PENDING_STATUS) {
      setTimeout(updateTaskResult, updateTime);
    }
  }
  async function cancel() {
    await deleteTaskResult(cm, task);
  }
  function formatTaskID(task) {
    return task.id.slice(0, 5) + '...';
  }
  function chartidFrom(task){
    return task.id.replaceAll("-","");
  }
  function plotDataForScatter(data){
    var result = [];
    for (var i = 0; i < data.length; i++) {
      result.push({ "y" : data[i] });
    }
    return result;
  }
function sortData(input){

    var data_sort = [];
    var switch_array = {};
    var output_array = {};

    data_sort = Object.values(input[0]).sort((a, b) => a - b)

    for(var i = 0; i < data_sort.length; i++)
    {
        switch_array[ Object.values(input[0])[i] ] = Object.keys(input[0])[i] ;
    }
    for(var i = 0; i < data_sort.length; i++)
    {
        output_array[ switch_array[ data_sort[i] ] ] = data_sort[i] ;
    }
    if(output_array["count"]){
      delete output_array["count"];
    }
    return {"keys" : Object.keys(output_array), "values" :  Object.values(output_array) } ;

}
  $: {
    console.log(cm);
    console.log(task);
    if (!isTaskPending){
      //labels = Object.keys(JSON.parse(JSON.stringify(taskResult.result))[0]);
      data_graph = sortData(JSON.parse(JSON.stringify(taskResult.result)));
      labels = data_graph.keys;
      plot_data = data_graph.values;
      //plot_data = Object.values(JSON.parse(JSON.stringify(taskResult.result))[0]);
      chartid = chartidFrom(task);
      scatterData = plotDataForScatter(plot_data);
    }
  }
</script>
<style>
.cmresult {
  border-style: solid;
}
</style>
<div class="cmresult">
<dl>
  <dt>task_id</dt><dd>{formatTaskID(task)}</dd>
  <dt>status</dt><dd>{taskResult.status}</dd>
  {#if !isTaskPending}
    <dt>data : </dt>
    <dd>{Object.keys(JSON.parse(JSON.stringify(taskResult.result))[0])}</dd>

    <dt>labels : </dt>
    <dd>{Object.values(JSON.parse(JSON.stringify(taskResult.result))[0])}</dd>

    <dt>results : </dt>
    <dd>{JSON.stringify(taskResult.result)}</dd>

    <dt>DATA</dt>
    <dd>{plot_data}</dd>

    <dt>LABELS</dt>
    <dd>{labels}</dd>

    <dt>TASK</dt>
    <dd>{task.id}</dd>

    <Chart data={plot_data} labels={labels} />

  {/if}
</dl>
<button on:click|once={cancel} disabled={!isTaskPending}>Cancel task</button>
</div>