<script>
    import CMList from './components/CMList.svelte';
    import Map from './components/Map.svelte';
    import TopNav from './components/TopNav.svelte';
</script>

<style>
:global(body) {
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
	width: 100%;
	height: 100%;
	display: flex;
}
:global(.close_button) {
  right: 0;
  position: absolute;
  padding: 3px;
  display: block;
  height: 30px;
  width: 30px;
  background-repeat: no-repeat;
  background-size: cover;
  background: url('/images/clear-icon.png');
}
</style>

<TopNav/>
<div id="main">
  <Map/>
  <CMList/>
</div>
