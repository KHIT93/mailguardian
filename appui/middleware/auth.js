export default defineNuxtRouteMiddleware((to, from) => {
    const { $auth } = useNuxtApp()
    if (!$auth().isAuthenticated()) {
        return navigateTo('/login')
    }

    return
})