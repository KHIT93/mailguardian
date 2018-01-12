import Vue from 'vue';
import axios from 'axios';
import components from './components/global_components';
import * as moment from 'moment';
import Nl2br from 'vue-nl2br';

window.Vue = Vue;
window.moment = moment;
Vue.component('nl2br', Nl2br)

import {store} from './vuex/store';

let Cookies = require('js-cookie');
window.Cookies = Cookies;

import router from './routing/router';

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

Vue.filter('yesno', value => {
    return value ? 'Yes' : 'No';
});

Vue.filter('byte_display', value => {
    let kb = 1024;
    let mb = 1024 * 1024;
    let gb = 1024 * 1024 * 1024;
    if (value < kb) {
        return value + ' B';
    }
    else if (value >= kb && value < mb) {
        return (value / kb).toFixed(2) + ' KB';
    }
    else if (value >= mb && value < gb) {
        return (value / mb).toFixed(2) + ' MB';
    }
    else {
        return (value / gb).toFixed(2) + ' GB';
    }
});

/**
 * Next, we will create a fresh Vue application instance and attach it to
 * the page. Then, you may begin adding components to this application
 * or customize the JavaScript scaffolding to fit your unique needs.
 */

 import { mapGetters, mapActions, mapMutations } from 'vuex';

const app = new Vue({
    el: '#app',
    router,
    store,
    components,
    mounted() {
        this.checkSession().then(() => {

            if (this.user.id) {
                console.log('Getting current user');
            }
            else {
                console.log('Redirecting to login');
                router.push('/login');
            }
        }).catch(() => {
            console.log('Redirecting to login');
            router.push('/login');
        });
        

    },
    methods: {
        ...mapActions(['checkSession', 'getCurrentUser']),
        ...mapMutations(['toggleLoading'])
    },
    computed: {
        ...mapGetters(['loading', 'isLoggedIn', 'user'])
    }
});