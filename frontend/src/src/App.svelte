<script>
    import CMList from './components/CMList.svelte';
    import Map from './components/Map.svelte';
    import Chart from './components/Chart.svelte';

</script>

<style>
body {
	margin-bottom: 20px;
	width: 100%;
	height: 100%;
}
#main {
	margin-bottom: 20px;
	width: 100%;
	height: 100%;
	display: flex;
}
</style>
<div id="main">
<Map/>
<CMList/>
</div>