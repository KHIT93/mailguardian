// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: {
      enabled: true
  },

  modules: [
      '@nuxt/ui',
    //   'nuxt-security',
      '@nuxt-alt/auth'
  ],

  app: {
      head: {
          title: 'MailGuardian',
          bodyAttrs: {
              class: 'bg-slate-100'
          }
      }
  },

  auth: {
      strategies: {
          local: {
              token: {
                  property: 'access_token',
                  global: true,
                  required: true,
                  name: 'Authorization',
                  type: 'Bearer',
                  httpOnly: true
              },
              user: {
                  property: false,
                  autoFetch: true
              },
              endpoints: {
                  login: { url: 'http://localhost:8000/api/v2/auth/token', method: 'post' },
                  logout: false,
                  user: { url: 'http://localhost:8000/api/v2/auth/whoami', method: 'get' }
              }
          }
      },
      globalMiddleware: true,
      redirect: {
          login: '/login',
          logout: '/login',
          home: '/'
      }
  },

  compatibilityDate: '2024-08-15'
})