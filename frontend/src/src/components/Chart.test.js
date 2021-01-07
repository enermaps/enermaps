import { test } from 'uvu'

import { render } from '@testing-library/svelte'
  import * as assert from 'uvu/assert'
import Chart from './Chart.svelte'

test('an empty dataset should render and empty graph', () => {
  const chart = render(Chart, {'datasets': []})
  console.log(chart);

});

test.run()
