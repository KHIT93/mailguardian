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
            this.authToken = token
        }
    }
})

export const useStatisticsStore = defineStore('statistics', {
    state: () => {
        return {
            allFilters: [],
            activeFilters: []
        }
    },
    getters: {
        getActiveFilters: (state) => state.activeFilters,
        getAllFilters: (state) => state.allFilters,
        getAvailableFilters: (state) => {
            return state.allFilters.filter(filter => {
                return !state.activeFilters.some(activeFilter => activeFilter.name == filter.name)
            })
        },
        hasActiveFilter: (state) => (filterName) => state.activeFilters.findIndex(filter => filter.name == filterName) > -1
    },
    actions: {
        setActiveFilter(filterObject) {
            this.activeFilters.push(filterObject)
        },
        async getFiltersFromBackend() {
            this.allFilters = (await useBackendFetch(`/api/reports/filters/`))
        },
        removeActiveFilter(filterIndex) {
            this.activeFilters.splice(filterIndex, 1)
        },
        removeActiveFilterByName(filterName) {
            this.activeFilters.splice(this.activeFilters.findIndex(filter => filter.name == filterName))
        }
    }
})

export const useApiStore = defineStore('api', {
    state: () => {
        return {
            loading: false
        }
    },
    getters: {
        isLoading: (state) => state.loading
    },
    actions: {
        toggleLoading(value) {
            this.loading = value
        }
    }
})