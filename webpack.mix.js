let mix = require('laravel-mix');
let tailwindcss = require('tailwindcss');

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

mix.js('./assets/src/js/app.js', './assets/dist/js')
   .less('./assets/src/css/app.less', './assets/dist/css').options({
       postCss: [
           tailwindcss('./mailware.js'),
       ]
   });
