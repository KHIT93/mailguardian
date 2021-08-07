import { createApp } from 'vue'
import App from './App.vue'
import './main.css'
import router from './router'
import auth from './auth'
import axios from 'axios'
import Cookies from 'js-cookie'

/**
 * We'll load the axios HTTP library which allows us to easily issue requests
 * to our Laravel back-end. This library automatically handles sending the
 * CSRF token as a header based on the value of the "XSRF" token cookie.
 */

 window.axios = axios;

 window.axios.interceptors.request.use(request => {
     if(process.env.NODE_ENV != "production") {
         console.log('Starting Request', request);
     }
     if (!request.url.includes('github')) {
         request.headers['X-CSRFToken'] = Cookies.get('csrftoken');
         request.headers['X-Requested-With'] = 'XMLHttpRequest';
     }
     return request;
 });
 window.axios.interceptors.response.use(response => {
     if(process.env.NODE_ENV != "production") {
         console.log('Response for previous request to ' + response.request.responseURL + ': ', response);
     }
     return response;
 });

createApp(App).use(router).use(auth).mount('#app')