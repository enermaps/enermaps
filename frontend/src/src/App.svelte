<script>
    import CMList from './components/CMList.svelte';
    import Map from './components/Map.svelte';
</script>

<style>
:global(body) {
	margin-bottom: 20px;
	width: 100%;
	height: 100%;
}
:global(.close_button) {
  float: right;
  padding: 3px;
  display: block;
  height: 30px;
  width: 30px;
  background-repeat: no-repeat;
  background-size: cover;
  background: url('/images/clear-icon.png');
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
