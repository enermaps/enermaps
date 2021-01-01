const { addHook } = require('pirates')
const svelte = require('svelte/compiler')

function handleSvelte(code) {
  const { js } = svelte.compile(code, {
    accessors: true,
    dev: true,
    format: 'cjs',
  })

  return js.code
}

addHook(handleSvelte, { exts: ['.svelte'] })