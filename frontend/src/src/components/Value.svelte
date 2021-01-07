<script>
export let value;
let name;
let formattedValue;
$ : {
  name = value[0];
  if (typeof value[1] === 'number') {
    formattedValue = String(value[1]);
  } else {
    formattedValue = value[1].join(' ');
  }
}
</script>

<dt>{name}</dt>
<dd>{formattedValue}</dd>
