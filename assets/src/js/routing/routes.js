/**
 * Import Vue components to use for Vue-Router
 */
import NotFound from '../pages/NotFound.vue';
import Home from '../pages/Home.vue';
import Login from '../pages/Login.vue';
import Messages from '../pages/Messages/Index.vue';
import MessageDetails from '../pages/Messages/Detail.vue';
import Lists from '../pages/Lists/Index.vue';
import Reports from '../pages/Reports/Index.vue';

export default [
    { path: '/', component: Home, name: 'home' },
    { path: '/login', component: Login, name: 'login' },
    { path: '/messages', component: Messages, name: 'messages.index' },
    { path: '/messages/:uuid', component: MessageDetails, name: 'messages.detail', props: true },
    { path: '/lists', component: Lists, name: 'lists' },
    { path: '/reports', component: Reports, name: 'reports' },

    /** Catchall route to display 404 page */
    { path: '*', component: NotFound, name: 'not_found' }
]