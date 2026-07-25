export default defineNuxtConfig({
  extends: 'content-wind',
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
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Friends of Woodmont Park is a new nonprofit dedicated to preserving, protecting, and promoting quality of life in the Woodmont neighborhood of North Chesterfield, Virginia.' },
      ],
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
      ],
      script: [
        {
          type: 'application/ld+json',
          innerHTML: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'NGO',
            name: 'Friends of Woodmont Park',
            alternateName: 'FWP',
            url: 'https://woodmontfriends.github.io',
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
