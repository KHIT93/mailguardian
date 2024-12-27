export default defineNuxtPlugin(() => {
    const { tokenStrategy } = useAuth()
    const runtimeConfig = useRuntimeConfig()
    const $backend = $fetch.create({
      baseURL: runtimeConfig.public.apiBaseUrl,
      onRequest({ request, options, error }) {
        if (tokenStrategy.token?.get()) {
          // Add Authorization header
          options.headers = options.headers || {}
          options.headers.set('Authorization', tokenStrategy.token?.get())
        }
      },
      // onResponseError({ response }) {
      //   if (response.status === 401) {
      //     return navigateTo('/login')
      //   }
      // }
    })
    // Expose to useNuxtApp().$backend
    return {
      provide: {
        backend: $backend
      }
    }
  })