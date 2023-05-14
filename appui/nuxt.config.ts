export default defineNuxtConfig({
    modules: [
        '@nuxtjs/tailwindcss',
        '@pinia/nuxt'
    ],
    ssr: false, // Seems to be required for some reason. Maybe the issue is fixed at RTM of Nuxt 3
    app: {
        head: {
            title: 'MailGuardian'
        }
    }
})
