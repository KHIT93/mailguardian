import Vue from 'vue';
import axios from 'axios';
import VueRouter from 'vue-router';
import * as moment from 'moment';

window.Vue = Vue;
window.moment = moment;
Vue.use(VueRouter);

import {store} from './vuex/store';

let Cookies = require('js-cookie');

import routes from './routing/routes';

const router = new VueRouter({
    routes
});

/**
 * We'll load the axios HTTP library which allows us to easily issue requests
 * to our Laravel back-end. This library automatically handles sending the
 * CSRF token as a header based on the value of the "XSRF" token cookie.
 */

window.axios = axios;

window.axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
window.axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

 /**
  * Debug code for logging AJAX calls to the console
  */
if(process.env.NODE_ENV != "production") {
    window.axios.interceptors.request.use(request => {
        console.log('Starting Request', request);
        return request;
    });
}

/**
 * Global helper method to perform redirection inside the application
 */
window.redirect = function(url) {
    router.push(url);
}

/**
 * Next, we will create a fresh Vue application instance and attach it to
 * the page. Then, you may begin adding components to this application
 * or customize the JavaScript scaffolding to fit your unique needs.
 */

const app = new Vue({
    el: '#app',
    router,
    store,
    components: {}
});