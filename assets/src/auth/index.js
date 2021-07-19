import axios from 'axios'
import { createAuth } from '@websanova/vue-auth'
import driverHttpAxios from '@websanova/vue-auth/dist/drivers/http/axios.1.x.esm.js'
import driverRouterVueRouter from '@websanova/vue-auth/dist/drivers/router/vue-router.2.x.esm.js'
import router from '../router'
import authToken from './drviers/token';

const auth = createAuth({
    plugins: {
        http: axios,
        router: router
    },
    stores: ['storage'],
    drivers: {
        http: driverHttpAxios,
        router: driverRouterVueRouter,
        auth: authToken
    },
    options: {
        loginData: {
            url: '/rest-auth/login/',
            staySignedIn: true,
        },
        logoutData: {
            url: '/rest-auth/logout/',
            redirect: '/login',
            makeRequest: true
        },
        fetchData: {
            url: '/rest-auth/user/'
        },
        refreshData: {
            enabled: false,
            url: '/rest-auth/user/'
        }
    }
})

export default auth