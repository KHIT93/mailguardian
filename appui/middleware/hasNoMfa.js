export default defineNuxtRouteMiddleware(async (to, from) => {
    const { $auth } = useNuxtApp()
    const currentUser = (await $auth().fetch())
    if (currentUser.has_two_factor) {
        return navigateTo('/mfa/enable')
    }

    return
})