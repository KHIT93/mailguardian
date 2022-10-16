import { useAuthenticationStore, useApiStore } from '~/store'
import { useSessionStorage } from '@vueuse/core'

const defaultOptions = {
    baseURL: 'http://localhost:8000' // TODO: Make this configurable somehow
}

export const useBackendFetch = (url, options = {}) => {
    options = {...defaultOptions, ...options}
    const nuxtApp = useNuxtApp()
    const authenticationStore = useAuthenticationStore(nuxtApp.$pinia)
    const apiStore = useApiStore(nuxtApp.$pinia)
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
    options.onRequest = ({ request, options }) => {
        apiStore.toggleLoading(true)
    }
    options.onResponse = ({ request, options, response }) => {
        apiStore.toggleLoading(false)
    }

    return $fetch(url, options)
}