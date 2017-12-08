/**
 * Import Vue components to use for Vue-Router
 */
import NotFound from '../pages/NotFound.vue';
import Home from '../pages/Home.vue';
import Login from '../pages/Login.vue';

export default {
    routes: [
        { path: '/', component: Home, name: 'home' },
        { path: '/login', component: Login, name: 'login' },

        /** Catchall route to display 404 page */
        { path: '*', component: NotFound, name: 'not_found' }
    ]
}