// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  app: {
    head: {
      charset: "utf-8",
      viewport: "width=device-width, initial-scale=1",
    },
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || "http://127.0.0.1:8000",
    },
  },

  ignore: [
    "**/*.stories.{js,cts,mts,ts,jsx,tsx}",
    "**/*.{spec,test}.{js,cts,mts,ts,jsx,tsx}",
    "**/*.d.{cts,mts,ts}",
    "**/.{pnpm-store,vercel,netlify,output,git,cache,data}",
    ".nuxt/analyze",
    ".nuxt",
    "**/-*.*",
    "node_modules",
  ],

  css: ["~/assets/css/main.css"],
  modules: [
    "@nuxtjs/tailwindcss", // https://tailwindcsss.nuxtjs.org
    "@sidebase/nuxt-auth", // https://sidebase.io/nuxt-auth/getting-started/quick-start
  ],

  // Module configs
  auth: {
    // https://sidebase.io/nuxt-auth/configuration/nuxt-config
    baseURL: process.env.AUTH_BASE || "http://127.0.0.1:8000/auth",
    provider: {
      type: "local",
      endpoints: {
        signIn: { path: "/token", method: "post" },
        // signOut: { path: "/logout", method: "post" },
        // signUp: { path: "/register", method: "post" },
        getSession: { path: "/profile", method: "get" },
      },
      pages: {
        login: "/auth/login",
      },
      token: {
        signInResponseTokenPointer: "/access",
        headerName: "Authorization",
        type: "Bearer",
        // maxAgeInSeconds: 0,
        sameSiteAttribute: "strict",
      },
      sessionDataType: {
        // TODO
        id: "number",
        username: "string",
        // last_login: null,
        // is_active: true,
        is_admin: true,
        // id: "string",
      },
    },
    session: {
      enableRefreshOnWindowFocus: false,
      enableRefreshPeriodically: 5 * 60 * 1000, // milliseconds
    },
    globalAppMiddleware: {
      isEnabled: true,
    },
  },
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  tailwindcss: {
    cssPath: "~/assets/css/main.css",
    configPath: "tailwind.config.js",
  },

  routeRules: {
    "/**": { cors: true },
  },
  typescript: {
    typeCheck: true,
    strict: true,
  },

  experimental: {
    watcher: "chokidar",
  },
});
