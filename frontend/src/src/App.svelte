<script>
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

  :global(.close_button) {
    padding: 3px;
    height: 25px;
    width: 25px;
    background-repeat: no-repeat;
    background-size: cover;
    box-sizing: border-box;
  }
</style>


<div id="main">
  <Map/>
</div>
