import { defineStore } from 'pinia'
import { useSessionStorage } from '@vueuse/core'

export const useAuthenticationStore = defineStore('authentication', {
    state: () => {
        return {
            user: {},
            authToken: useSessionStorage('authToken')
        }
    },
    getters: {
        getUser: (state) => state.user,
        getAuthToken: (state) => state.authToken
    },
    actions: {
        setUser(userObject) {
            this.user = userObject
        },
        setAuthToken(token) {
            let dataToken = useSessionStorage('authToken', token)
            console.log(dataToken)
            this.authToken = token
        }
    }
})