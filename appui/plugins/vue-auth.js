import Auth from '~/auth'

export default defineNuxtPlugin((nuxtApp) => {
    nuxtApp.vueApp.use(Auth)
})