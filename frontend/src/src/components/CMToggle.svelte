<script>
import { isCMPaneActiveStore } from '../stores.js';
function toggleCM() {
  isCMPaneActiveStore.update(n => !n);
}
</script>
<style>
#cm_toggle {
  height: 100%;
  width: 100%;
  display: block;
  cursor: pointer;
}
#cm_toggle_container:hover {
  background-color: #f4f4f4;
  background: url('../analytics_icon.png') #fafafa;
}
#cm_toggle_container {
  background-repeat: no-repeat;
  background-size: cover;
  background: url('../analytics_icon.png');
  height: 30px;
  width: 30px;
  background-color: white;
  padding: 4px;
  border-radius: 4px;
  border: 2px solid rgba(0,0,0,0.2);
}
</style>
<div id="cm_toggle_container">
<a id="cm_toggle" title="Display CM" on:click={toggleCM}>
</a>
</div>
