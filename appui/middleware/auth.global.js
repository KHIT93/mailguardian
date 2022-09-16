const GUEST_ROUTES = [
    '/login',
    '/password/reset'
]

export default defineNuxtRouteMiddleware((to, from) => {
    const { $auth } = useNuxtApp()
    if (GUEST_ROUTES.includes(to.fullPath)) {
        return
    }
    if (!$auth().isAuthenticated()) {
        return navigateTo('/login')
    }

    return
})