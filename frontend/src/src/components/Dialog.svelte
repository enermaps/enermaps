<script >
  import {onMount} from 'svelte';

  export let title = '';

  let dialog;


  onMount(async () => {
    const closeButton = dialog.getElementsByClassName('close')[0];

    // When the user clicks on <span> (x), close the modal
    closeButton.onclick = function() {
      dialog.style.display = 'none';
    };

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == dialog) {
        dialog.style.display = 'none';
      }
    };
  });


  export function show() {
    dialog.style.display = 'block';
  }

</script>


<style>
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

  .modal-content {
    position: relative;
    background-color: #eff4fa;
    margin: auto;
    padding: 0;
    border: 1px solid #888;
    width: 60%;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2),0 6px 20px 0 rgba(0,0,0,0.19);
  }

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
    padding: 0px 60px;
    background-color: #eff4fa;
    color: #27275b;
    cursor: default;
  }

  .modal-body {
    padding: 0px 60px;
    background-color: #eff4fa;
    color: #27275b;
    text-align: justify;
    text-justify: inter-word;
    cursor: default;
  }
</style>


<div class="modal" bind:this={dialog}>
  <div class="modal-content">
    <div class="close">&times;</div>
    <div class="modal-header">
      <h2>{ title }</h2>
    </div>
    <div class="modal-body">
      <slot></slot>
    </div>
  </div>
</div>
