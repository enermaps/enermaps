<script>
export let value;
let name;
let formattedValue;

$ : {
  name = value[0];
  console.log(value);
  if (Array.isArray(value[1])) {
    formattedValue = value[1].map(String).join(' ');
  } else {
    formattedValue = String(value[1]);
  }
}
</script>

<dt>{name}</dt>
<dd>{formattedValue}</dd>
