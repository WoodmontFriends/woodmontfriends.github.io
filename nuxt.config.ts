// Google Analytics 4 measurement ID for woodmontfriends.org (G-XXXXXXXXXX). The tag stays off until it's set.
const gaMeasurementId = ''

export default defineNuxtConfig({
  extends: 'content-wind',
  modules: ['nuxt-gtag'],
  css: ['~/assets/css/park.css'],
  gtag: {
    // GA4 enhanced measurement (on by default) also records outbound clicks, such as to the sign-up form.
    id: gaMeasurementId,
    enabled: Boolean(gaMeasurementId),
  },
  colorMode: {
    preference: 'light',
    fallback: 'light',
  },
  nitro: {
    prerender: {
      failOnError: false,
    },
  },
  app: {
    head: {
      htmlAttrs: {
        lang: 'en',
      },
      meta: [
        { name: 'theme-color', content: '#1f3a2e' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Friends of Woodmont Park is a new nonprofit dedicated to preserving, protecting, and promoting quality of life in the Woodmont neighborhood of North Chesterfield, Virginia.' },
      ],
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;600;700&family=Zilla+Slab:wght@500;600;700&display=swap' },
      ],
      script: [
        {
          type: 'application/ld+json',
          innerHTML: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'NGO',
            name: 'Friends of Woodmont Park',
            alternateName: 'FWP',
            url: 'https://woodmontfriends.org',
            description: 'A Virginia nonprofit corporation preserving, protecting, and promoting quality of life in the Woodmont neighborhood of North Chesterfield, VA through sustainable improvements and collective community effort.',
            nonprofitStatus: 'NonprofitType',
            areaServed: {
              '@type': 'Place',
              name: 'Woodmont, North Chesterfield, Virginia',
            },
            sameAs: [
              'https://github.com/WoodmontFriends',
            ],
          }),
        },
      ],
    },
  },
})
