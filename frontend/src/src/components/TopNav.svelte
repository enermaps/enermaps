<script context="module">
  import 'leaflet-search/dist/leaflet-search.src.js';
  import 'leaflet-search/dist/leaflet-search.src.css';
</script>

<style>

#topnav {
  background-color: #27275b;
  overflow: visible;
  padding: 8px 20px;
  display: inline-block;
}

#topnav div {
  color: #eff4fa;
  text-align: center;
  text-decoration: none;
  font-size: 32px;
  box-sizing: border-box;
  vertical-align: middle;
  display: inline-block;
}

.link {
  font-size: 24px;
  color: #eff4fa;
  display: inline-block;
  vertical-align: middle;
  text-decoration: none;
  margin-left: 30px;
}

.link:hover{
  text-decoration: underline;
  text-decoration-thickness: 2.5px;
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

#slot {
  vertical-align: middle;
  display: inline-block;
  box-sizing: border-box;
}



</style>

<div id="topnav">
  <div id='logo'> <img src='images/logo.png' alt='EnerMaps'> </div>
  <div id='title'>EnerMaps</div>
  <slot id='slot'></slot>
  <a href="https://enermaps.eu/" target="_blank" class="link">Wiki</a>
  <a href="https://beta.enermaps.openaire.eu/" target="_blank" class="link">OpenAIRE</a>
  <a href="https://enermaps.eu/" target="_blank" class="link">About</a>
</div> 