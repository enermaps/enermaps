<script >
  import {onMount} from 'svelte';
  import 'leaflet-search/dist/leaflet-search.src.js';
  import 'leaflet-search/dist/leaflet-search.src.css';

  let btn;
  let modal;
  let span;

  onMount(async () => {
    // Get the modal
    modal = document.getElementById('myModal');
    // Get the button that opens the modal
    btn = document.getElementById('myBtn');
    // Get the <span> element that closes the modal
    span = document.getElementsByClassName('close')[0];
    // When the user clicks the button, open the modal
    btn.onclick = function() {
      modal.style.display = 'block';
    };
    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
      modal.style.display = 'none';
    };
    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = 'none';
      }
    };
  });
</script>


<style>
  #topnav {
    background-color: #27275b;
    overflow: visible;
    padding: 8px 20px;
    display: inline-block;
  }

  #topnav div {
    text-align: center;
    text-decoration: none;
    box-sizing: border-box;
    vertical-align: middle;
  }

  #topnav div.top,
  #topnav div.top div {
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
    display: inline-block;
    vertical-align: middle;
  }

  #title {
    color: #eff4fa;
    font-size: 22px;
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

  /* The Modal (background) */
  .modal {
    display: none; /* Hidden by default */
    position: fixed; /* Stay in place */
    z-index: 99999999; /* Sit on top */
    padding-top: 100px; /* Location of the box */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgb(0,0,0); /* Fallback color */
    background-color: rgba(0,0,0,0.5); /* Black w/ opacity */
  }

  /* Modal Content */
  .modal-content {
    position: relative;
    background-color: #eff4fa;
    margin: auto;
    padding: 0;
    border: 1px solid #888;
    width: 60%;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2),0 6px 20px 0 rgba(0,0,0,0.19);
  }

  /* The Close Button */
  .close {
    color: #27275b;
    font-size: 40px;
    position:absolute;
    height: 50px;
    width: 50px;
    line-height: 50px;

    display: flex !important;
    align-items: center; /* Vertical center alignment */
    justify-content: center; /* Horizontal center alignment */
  }

  .close:hover,
  .close:focus {
    text-decoration: none;
    cursor: pointer;
  }

  .modal-header {
    padding: 0px 45px;
    background-color: #eff4fa;
    color: #27275b;
    width: 100%;
    cursor: default;
  }

  .modal-body {
    padding: 0px 60px;
    background-color: #eff4fa;
    color: #27275b;
    width: 100%;
    text-align: justify;
    text-justify: inter-word;
    cursor: default;
  }

  button, button:hover {
    font-family: inherit;
    border: 0;
    padding: 0;
    background-color: inherit;
  }
</style>


<div id="topnav">
  <div class="top">
    <div id='logo'> <img src='images/logo.png' alt='EnerMaps'> </div>
    <div id='title'>EnerMaps</div>
  </div>

  <a href="https://enermaps.eu/" target="_blank" class="link">Wiki</a>
  <a href="https://beta.enermaps.openaire.eu/" target="_blank" class="link">OpenAIRE</a>
  <a href="https://www.kialo.com/" target="_blank" class="link">Kialo</a>
  <!-- Trigger/Open The Modal -->
  <button id="myBtn" class="link">About</button>
  <slot id='slot'></slot>

  <!-- The Modal -->
  <div id="myModal" class="modal">
    <!-- Modal content -->
    <div class="modal-content">
      <div class="close">&times;</div>
      <div class="modal-header">
        <h2 >About EnerMaps</h2>
      </div>
      <div class="modal-body">
        <p>
          EnerMaps Open Data Management Tool aims to improve data management and
          accessibility in the field of energy research for the renewable energy industry.
        </p>
        <p>
          EnerMaps’ tool accelerates and facilitates the energy transition offering a
          qualitative and user-friendly digital platform to the energy professionals.
        </p>
        <p>
          The EnerMaps project has received funding from the European Union’s Horizon
          2020 research and innovation program under grant agreement N°884161.
        </p>
        <p>
      </div>
    </div>
  </div>

</div>
