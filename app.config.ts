export default defineAppConfig({
  // Configure Content Wind here
  cover: '/favicon.svg',
  email: 'info@woodmontfriends.org',
  // Google Form in the FWP Board Internal shared drive ("FWP Sign-ups (website + Fall Fest)")
  signupUrl: 'https://docs.google.com/forms/d/e/1FAIpQLSfnm6BANJCPeBfbAIajsnJIINk3fJl5o6F-wxD9--0qofDM4Q/viewform',
  // Public GitHub Projects board ("Community Roadmap")
  roadmapUrl: 'https://github.com/orgs/WoodmontFriends/projects/2',
  // Public projects feed from the admin app: cards labelled "public" (fwp-admin lib/public-board.ts)
  publicBoardUrl: 'https://admin.woodmontfriends.org/api/public/board',

  // Feature flags. A flag that's off can be previewed with ?flag=<name>, e.g. /nature?flag=natureMap
  features: {
    // Park nature map at /nature (sightings from iNaturalist). Turning it on also adds it to the header.
    natureMap: false,
    // Projects board at /projects, fed by the admin app. Turning it on adds it to the header and
    // points the footer's roadmap link there instead of GitHub.
    projectsBoard: false,
  },

  // Park nature map settings
  nature: {
    // iNaturalist project slug (the part after /projects/ in its URL). While empty, the map
    // shows iNaturalist observations inside the areas in data/nature-areas.ts instead.
    projectSlug: '',
    // Edible species people may harvest. They show as a rough area, never an exact pin.
    // Matched on the scientific name's first word (genus).
    protectedGenera: ['Cantharellus', 'Craterellus', 'Morchella', 'Grifola', 'Hericium', 'Laetiporus', 'Hydnum', 'Boletus'],
  },
})
