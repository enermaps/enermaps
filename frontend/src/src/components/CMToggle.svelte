<script>
import { isCMPaneActiveStore } from '../stores.js';
function toggleCM() {
  isCMPaneActiveStore.update(n => !n);
}
</script>
<style>
#cm_toggle {
  background: url('../analytics_icon.png');
  background-repeat: no-repeat;
  background-size: cover;
  height: 30px;
  width: 30px;
  display: inline-block;
}
#cm_toggle_container {
  background-color: white;
  padding: 4px;
  border-radius: 4px;
  background-clip: padding-box;
  cursor: auto;
  border: 2px solid rgba(0,0,0,0.2);
}
</style>
<div id="cm_toggle_container">
<a id="cm_toggle" title="Display CM" on:click={toggleCM}>
</a>
</div>
