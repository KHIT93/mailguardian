export default defineNuxtPlugin(() => {
    const { tokenStrategy } = useAuth()
    const $backend = $fetch.create({
      baseURL: 'http://localhost:8000/api/v2',
      onRequest({ request, options, error }) {
        if (tokenStrategy.token?.get()) {
          // Add Authorization header
          options.headers = options.headers || {}
          options.headers.Authorization = tokenStrategy.token?.get()
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