<script >
  import {onMount} from 'svelte';
  import 'leaflet-search/dist/leaflet-search.src.js';
  import 'leaflet-search/dist/leaflet-search.src.css';


  var btn;
  var modal;
  var span;

  onMount(async () => {
    // Get the modal
     modal = document.getElementById("myModal");
    // Get the button that opens the modal
     btn = document.getElementById("myBtn");
    // Get the <span> element that closes the modal
    span = document.getElementsByClassName("close")[0];

    // When the user clicks the button, open the modal 
    btn.onclick = function() {
      modal.style.display = "block";
    }

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
      modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
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
  color: #eff4fa;
  display: inline-block;
  vertical-align: middle;
  box-sizing: border-box;
  font-size: 32px;
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
  width: 80%;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2),0 6px 20px 0 rgba(0,0,0,0.19);

}

/* The Close Button */
.close {
  color: #27275b;
  font-size: 55px;
  position:absolute;
  top: 0px;
  right: 0px;
}

.close:hover,
.close:focus {
  text-decoration: none;
  cursor: pointer;
}

.modal-header {
  padding: 10px 45px;
  background-color: #eff4fa;
  color: #27275b;
  width: 100%;
  cursor: default;
}

.modal-body {
  padding: 0px 45px;
  background-color: #eff4fa;
  color: #27275b;
  width: 100%;
  text-align: justify;
  text-justify: inter-word;
  cursor: default;
  }

.modal-footer {
  padding: 10px 45px;
  background-color: #eff4fa;
  color: #27275b;
  width: 100%;
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
  <div id='logo'> <img src='images/logo.png' alt='EnerMaps'> </div>
  <div id='title'>EnerMaps</div>
  <slot id='slot'></slot>
  <a href="https://enermaps.eu/" target="_blank" class="link">Wiki</a>
  <a href="https://beta.enermaps.openaire.eu/" target="_blank" class="link">OpenAIRE</a>
  <!-- Trigger/Open The Modal -->
  <button id="myBtn" class="link">About</button>

  <!-- The Modal -->
<div id="myModal" class="modal">
  <!-- Modal content -->
  <div class="modal-content">
    <div class="modal-header">
      <span class="close">&times;</span>
      <h2 >About EnerMaps</h2>
    </div>
    <div class="modal-body">
      <p>
        Intellectum est enim mihi quidem in multis, et maxime in me ipso, sed paulo ante in omnibus, 
        cum M. Marcellum senatui reique publicae concessisti, commemoratis praesertim offensionibus, 
        te auctoritatem huius ordinis dignitatemque rei publicae tuis vel doloribus vel suspicionibus anteferre.
        Ille quidem fructum omnis ante actae vitae hodierno die maximum cepit, cum summo consensu senatus, tum iudicio 
        tuo gravissimo et maximo.
        Ex quo profecto intellegis quanta in dato beneficio sit laus, cum in accepto sit tanta gloria.
      </p>
      <p>
        Nunc vero inanes flatus quorundam vile esse quicquid extra urbis pomerium 
        nascitur aestimant praeter orbos et caelibes, nec credi potest qua obsequiorum
         diversitate coluntur homines sine liberis Romae.
      </p>
      <p>
        Principium autem unde latius se funditabat, emersit ex negotio tali. 
        Chilo ex vicario et coniux eius Maxima nomine, questi apud Olybrium ea tempestate urbi praefectum, 
        vitamque suam venenis petitam adseverantes inpetrarunt ut hi, quos suspectati sunt, ilico rapti 
        conpingerentur in vincula, organarius Sericus et Asbolius palaestrita et aruspex Campensis.
      </p>
      <p>
        Novitates autem si spem adferunt, ut tamquam in herbis non fallacibus fructus appareat, non sunt 
        illae quidem repudiandae, vetustas tamen suo loco conservanda; maxima est enim vis vetustatis et 
        consuetudinis. Quin in ipso equo, cuius modo feci mentionem, si nulla res impediat, nemo est, quin eo, 
        quo consuevit, libentius utatur quam intractato et novo. Nec vero in hoc quod est animal, sed in iis etiam 
        quae sunt inanima, consuetudo valet, cum locis ipsis delectemur, montuosis etiam et silvestribus, in quibus 
        diutius commorati sumus.
      </p>
    </div>
    <div class="modal-footer">
      <h3>Modal Footer</h3>
    </div>
  </div>
</div>

</div> 



