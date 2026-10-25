export default defineAppConfig({
  // Configure Content Wind here
  cover: '/favicon.svg',
  email: 'info@woodmontfriends.org',
  // Google Form in the FWP Board Internal shared drive ("FWP Sign-ups (website + Fall Fest)")
  signupUrl: 'https://docs.google.com/forms/d/e/1FAIpQLSfnm6BANJCPeBfbAIajsnJIINk3fJl5o6F-wxD9--0qofDM4Q/viewform',
  // Public GitHub Projects board ("Community Roadmap")
  roadmapUrl: 'https://github.com/orgs/WoodmontFriends/projects/2',

  // Feature flags. A flag that's off can be previewed with ?flag=<name>, e.g. /nature?flag=natureMap
  features: {
    // Park nature map at /nature (sightings from iNaturalist). Turning it on also adds it to the header.
    natureMap: false,
  },

  // Park nature map settings
  nature: {
    // iNaturalist project slug (the part after /projects/ in its URL). While empty, the map
    // shows every iNaturalist observation inside `bounds` instead.
    projectSlug: '',
    // Rough box around the park; used for the search above and to frame the map.
    bounds: { swlat: 37.5225, swlng: -77.5925, nelat: 37.5315, nelng: -77.5805 },
    // Woodmont pool, 2334 Traymore Rd
    center: [37.5272, -77.5863] as [number, number],
    zoom: 16,
    // Edible species people may harvest. They show as a rough area, never an exact pin.
    // Matched on the scientific name's first word (genus).
    protectedGenera: ['Cantharellus', 'Craterellus', 'Morchella', 'Grifola', 'Hericium', 'Laetiporus', 'Hydnum', 'Boletus'],
  },
})
