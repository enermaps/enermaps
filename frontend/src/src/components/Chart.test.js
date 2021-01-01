import { test } from 'uvu'

import { render } from '@testing-library/svelte'
import Chart from './Chart.svelte'

test('should do stuff', () => {
  const chart = render(Chart, {'datasets': []})

});

test.run()
