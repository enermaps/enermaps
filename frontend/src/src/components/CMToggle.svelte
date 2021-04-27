<script>
import {isCMPaneActiveStore} from '../stores.js';
function toggleCM() {
  isCMPaneActiveStore.update((n) => !n);
}
</script>
<style>
#cm_toggle {
  height: 100%;
  width: 100%;
  display: block;
  cursor: pointer;
}

#cm_toggle_container {
  background-repeat: no-repeat;
  background-size: cover;
  height: 45px;
  width: 45px;
  box-sizing: border-box;
  background-color: #eff4fa;
  padding: 4px;
  border-radius: 4px;
  border: 1px solid #27275b;
}
</style>
<div id="cm_toggle_container" hidden={$isCMPaneActiveStore}>
<a id="cm_toggle" title="Display CM" on:click|stopPropagation={toggleCM}>
</a>
</div>
