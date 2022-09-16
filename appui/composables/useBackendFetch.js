import { useAuthenticationStore } from '~/store'
import { useSessionStorage } from '@vueuse/core'

const defaultOptions = {
    baseURL: 'http://localhost:8000' // TODO: Make this configurable somehow
}

export const useBackendFetch = (url, options = {}) => {
    options = {...defaultOptions, ...options}
    const nuxtApp = useNuxtApp()
    const authenticationStore = useAuthenticationStore(nuxtApp.$pinia)
    let token = useSessionStorage('authToken').value
    if (nuxtApp.$auth().isAuthenticated()) {
        if (options.headers) {
            options.headers.Authorization = `Token ${token}`
        }
        else {
            options.headers = {
                Authorization: `Token ${token}`
            }
        }
    }

    return $fetch(url, options)
}