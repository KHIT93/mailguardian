import { useAuthenticationStore } from '~/store'
import { useSessionStorage } from '@vueuse/core'

const defaultOptions = {
    loginData: {
        url: '/rest-auth/login/',
        method: 'POST',
        redirect: '/',
        fetchUser: true,
        staySignedIn: true
    },
    fetchData: {
        url: '/rest-auth/user/',
        method: 'GET',
        enabled: true
    }
}

const fetchUser = (options, authenticationStore) => {
    options = { ...defaultOptions.fetchData, ...options }
    let token = authenticationStore.getAuthToken
    return new Promise((resolve, reject) => {
        useBackendFetch(options.url).then(data => {
            authenticationStore.setUser(data)
            resolve(data)
        }, reject)
    })
}

const login = (options, authenticationStore) => {
    options = { ...defaultOptions.loginData, ...options }
    return new Promise((resolve, reject) => {
        useBackendFetch(options.url, {
            method: options.method,
            body:  options.data
        }).then((data) => {
            console.log(data)
            if (data.auth_token) {
                authenticationStore.setAuthToken(data.auth_token)
                let token = useSessionStorage('authToken', data.auth_token)
                token.value = data.auth_token
            }
            if (options.fetchUser) {
                fetchUser({}).then(resolve, reject)
            }
            else {
                resolve(data)
            }
        }, response => {
            console.error(response)
            reject(response)
        })
    })
}

export default defineNuxtPlugin(nuxtApp => {
    const authenticationStore = useAuthenticationStore(nuxtApp.$pinia)
    return {
        provide: {
            auth: () => {
                return {
                    login: options => {
                        return login(options, authenticationStore)
                    },
                    logout() {
            
                    },
                    fetch: options => {
                        return fetchUser(options, authenticationStore)
                    },
            
                    isAuthenticated() {
                        let token = useSessionStorage('authToken').value
                        if (!token) {
                            return false
                        }
                        else if (typeof token === 'undefined') {
                            return false
                        }
                        else if (token == 'undefined') {
                            return false
                        }
                        else {
                            return !! useSessionStorage('authToken').value
                        }
                    }
                }
            }
        }
    }
})