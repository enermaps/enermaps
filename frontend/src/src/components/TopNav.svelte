<script >
  import {onMount} from 'svelte';

  import 'leaflet-search/dist/leaflet-search.src.js';
  import 'leaflet-search/dist/leaflet-search.src.css';

  import Dialog from './Dialog.svelte';
  import About from '../popups/About.svelte';


  let aboutDialog = null;
  let copyPopup = null;


  onMount(async () => {
    const aboutButton = document.getElementById('btn_about');

    aboutButton.onclick = function() {
      aboutDialog.show();
    };

    aboutDialog.show();
  });


  function copyWMSUrlToClipboard(event) {
    // Create new temporary text element containing the value to copy
    const el = document.createElement('textarea');
    el.value = document.URL + 'api/wms';

    // Set non-editable to avoid focus and move outside of view
    el.setAttribute('readonly', '');
    el.style.position = 'absolute';
    el.style.left = '-9999px';
    document.body.appendChild(el);

    // Select text inside element
    el.select();

    // Copy text to clipboard
    document.execCommand('copy');

    // Remove temporary element
    document.body.removeChild(el);

    // Show the popup
    const rect = event.target.getBoundingClientRect();

    if (copyPopup === null) {
      copyPopup = document.createElement('div');
      copyPopup.textContent = 'URL copied to the clipboard';
      copyPopup.style.position = 'absolute';
      copyPopup.style.left = (rect.left - 10) + 'px';
      copyPopup.style.top = (rect.bottom + 6) + 'px';
      copyPopup.style.backgroundColor = 'lightgoldenrodyellow';
      copyPopup.style.fontSize = '14px';
      copyPopup.style.padding = '4px';
      document.body.appendChild(copyPopup);
    }
  }


  function hideCopyPopup() {
    if (copyPopup !== null) {
      document.body.removeChild(copyPopup);
      copyPopup = null;
    }
  }
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

  <a href="https://enermaps-wiki.herokuapp.com" target="_blank" class="link">Wiki</a>
  <a href="https://beta.enermaps.openaire.eu/" target="_blank" class="link">OpenAIRE</a>
  <a href="https://www.kialo.com/" target="_blank" class="link">Kialo</a>
  <button class="link" title="Copy the URL of the WMS server to the clipboard"
          on:click={copyWMSUrlToClipboard} on:mouseleave={hideCopyPopup}>WMS</button>
  <button id="btn_about" class="link">About</button>

  <slot id='slot'></slot>

  <Dialog title="About EnerMaps" bind:this={aboutDialog}>
    <About />
  </Dialog>

</div>
