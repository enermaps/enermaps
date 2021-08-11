<script>
    import CMList from './components/CMList.svelte';
    import Map from './components/Map.svelte';
</script>

<style>
:global(body) {
	width: 100%;
	height: 100%;
}
#main {
	width: 100%;
	height: 100%;
	display: flex;
}

/* :global(.close_button) {
  float: right;
  padding: 3px;
  display: block;
  height: 25px;
  width: 325x;
  background-repeat: no-repeat;
  background-size: cover;
  background: url('/images/clear-icon.png');
  cursor: pointer;
  box-sizing: border-box;
} */

:global(.close_button) {
  /* right: 0; */
  /* position: absolute; */
  padding: 3px;
  /* display: block; */
  height: 25px;
  width: 25px;
  background-repeat: no-repeat;
  background-size: cover;
  /* background: url('/images/clear-icon.png'); */
  box-sizing: border-box;
}
</style>
<div id="main">
<Map/>
<CMList/>
</div>
