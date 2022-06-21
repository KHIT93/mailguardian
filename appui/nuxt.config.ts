import { defineNuxtConfig } from 'nuxt'

// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
    modules: [
        '@nuxtjs/tailwindcss',
        '@pinia/nuxt'
    ],
    ssr: false // Seems to be required for some reason. Maybe the issue is fixed at RTM of Nuxt 3
})
