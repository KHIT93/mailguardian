let mix = require('laravel-mix');
let tailwindcss = require('tailwindcss');
let resolve = require('path').resolve

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 | Mix provides a clean, fluent API for defining some Webpack build steps
 | for your Laravel application. By default, we are compiling the Sass
 | file for your application, as well as bundling up your JS files.
 |
 */
mix.setPublicPath(resolve('./'));
mix.js('./assets/src/js/app.js', './assets/dist/js').vue({ version: 2 })
   .postCss('./assets/src/css/app.css', './assets/dist/css').options({
       postCss: [
           tailwindcss('./tailwind.config.js'),
       ]
   }).version();
