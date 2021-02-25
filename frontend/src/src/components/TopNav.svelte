<script context="module">
  import 'leaflet-search/dist/leaflet-search.src.js';
  import 'leaflet-search/dist/leaflet-search.src.css';


  //import {onMount} from 'svelte';

  //let topnav;

  /*
  onMount(async () => {

    topnav.addControl(makeSearchControl());
  });
  */
 
  export function makeSearchControl() {
  const searchControl = new L.Control.Search({
    url: 'https://nominatim.openstreetmap.org/search?format=json&q={s}',
    jsonpParam: 'json_callback',
    propertyName: 'display_name',
    propertyLoc: ['lat', 'lon'],
    marker: false, // L.circleMarker([0, 0], { radius: 30 }),
    autoCollapse: true,
    autoType: false,
    minLength: 2,
    container: "map_control"
  });
  return searchControl;
}

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
  <div id='map_control'> </div>
</div> 