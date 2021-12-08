import { createWebHistory, createRouter } from "vue-router"
import PagesIndex from '../pages/Index.vue'
import PagesLogin from '../pages/Login.vue'
import Messages from '../pages/messages/_id.vue'
import ListIndex from '../pages/lists/Index.vue'
import ListEdit from '../pages/lists/_id/edit.vue'
import UserIndex from '../pages/users/index.vue'
import UserCreate from '../pages/users/create.vue'
import UserEdit from '../pages/users/_id/edit.vue'
import DomainIndex from '../pages/domains/index.vue'
import DomainCreate from '../pages/domains/create.vue'
import DomainEdit from '../pages/domains/_id/edit.vue'
import AccountIndex from '../pages/account.vue'
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
        path: '/account',
        name: 'account.index',
        component: AccountIndex,
        meta: {
            auth: true
        }
    },

    {
        path: '/users',
        name: 'users.index',
        component: UserIndex,
        meta: {
            auth: true
        }
    },
    {
        path: '/users/create',
        name: 'users.create',
        component: UserCreate,
        meta: {
            auth: true
        }
    },
    {
        path: '/users/:id/edit',
        name: 'users.edit',
        component: UserEdit,
        meta: {
            auth: true
        }
    },

    {
        path: '/domains',
        name: 'domains.index',
        component: DomainIndex,
        meta: {
            auth: true
        }
    },
    {
        path: '/domains/create',
        name: 'domains.create',
        component: DomainCreate,
        meta: {
            auth: true
        }
    },
    {
        path: '/domains/:id/edit',
        name: 'domains.edit',
        component: DomainEdit,
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