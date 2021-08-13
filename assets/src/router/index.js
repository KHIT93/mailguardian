import { createWebHistory, createRouter } from "vue-router"
import PagesIndex from '../pages/Index.vue'
import PagesLogin from '../pages/Login.vue'
import Messages from '../pages/messages/_id.vue'
import ListIndex from '../pages/lists/Index.vue'
import ListEdit from '../pages/lists/_id/edit.vue'
import PageNotFound from '../pages/404.vue'

let routes = [
    {
        path: '/',
        name: 'home',
        component: PagesIndex,
        meta: {
            auth: true
        }
    },
    {
        path: '/login',
        name: 'login',
        component: PagesLogin,
        meta: {
            auth: false
        }
    },
    {
        path: '/messages/:id',
        name: 'messages.show',
        component: Messages,
        meta: {
            auth: true
        }
    },
    {
        path: '/lists',
        name: 'lists.index',
        component: ListIndex,
        meta: {
            auth: true
        }
    },
    {
        path: '/lists/:id/edit',
        name: 'lists.edit',
        component: ListEdit,
        meta: {
            auth: true
        }
    },

    {
        path: '/:pathMatch(.*)*',
        name: 'not-found',
        component: PageNotFound
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router