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
              url: `${process.env.SERVER_HOST}/api/v2`,
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
                  login: { url: `${process.env.SERVER_HOST}/api/v2/auth/token`, method: 'post' },
                  logout: false,
                  user: { url: `${process.env.SERVER_HOST}/api/v2/auth/whoami`, method: 'get' }
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

  runtimeConfig: {
    public: {
        apiBaseUrl: `${process.env.SERVER_HOST}/api/v2`
    }
  },

  compatibilityDate: '2024-08-15'
})