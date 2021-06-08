<script context="module">
  import 'leaflet-search/dist/leaflet-search.src.js';
  import 'leaflet-search/dist/leaflet-search.src.css';

  //import CMToggle from './CMToggle.svelte';

  // import {onMount} from 'svelte';

  //let topnav;

  // runs after the component is first rendered to the DOM
  /*
  onMount(async () => {
    toogle_div = makeCMToggleControl();
  });
  */
 

/*
function makeCMToggleControl() {
  const CMToggleControl = L.control({position: 'topright'});
  CMToggleControl.onAdd = (map) => {
    const div = L.DomUtil.create('div');
    L.DomUtil.addClass(div, 'test');
    toolbar = new CMToggle({target: div});
    return div;
  };
  return CMToggleControl;
}
*/

</script>

<style>

/* Add a black background color to the top navigation */

#topnav {
  background-color: #27275b;
  overflow: hidden;
  padding: 8px 20px;
}


/* Style the links inside the navigation bar */

#topnav div {
  color: #eff4fa;
  text-align: center;
  text-decoration: none;
  font-size: 32px;
  box-sizing: border-box;
  vertical-align: middle;
  display: inline-block;
}


#logo {
  box-sizing: border-box;
  height: 100%;
}

#title {
  display: inline-block;
  vertical-align: middle;
  box-sizing: border-box;
}

img {
  vertical-align: middle;
  display: inline-block;
  height: 40px;
  box-sizing: border-box;
}



</style>

<div id="topnav">
  <div id='logo'> <img src='images/logo.png' alt='EnerMaps'> </div>
  <span></span>
  <div id='title'>EnerMaps</div>
  <div id='cm_control'> 
  </div>
</div> 