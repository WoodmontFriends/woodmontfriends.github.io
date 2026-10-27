export default defineAppConfig({
  // Configure Content Wind here
  cover: '/favicon.svg',
  email: 'info@woodmontfriends.org',
  // Google Form in the FWP Board Internal shared drive ("FWP Sign-ups (website + Fall Fest)")
  signupUrl: 'https://docs.google.com/forms/d/e/1FAIpQLSfnm6BANJCPeBfbAIajsnJIINk3fJl5o6F-wxD9--0qofDM4Q/viewform',
  // Public projects feed from the admin app: cards labelled "public" (fwp-admin lib/public-board.ts)
  publicBoardUrl: 'https://admin.woodmontfriends.org/api/public/board',
  // Upcoming events on the public "FWP Community Events" Google Calendar, from the admin app
  publicEventsUrl: 'https://admin.woodmontfriends.org/api/public/events',
  // The public "FWP Community Events" Google Calendar (not secret). Used by ::calendar-callout.
  communityCalendarId: 'c_9b7954698fc7de9a49e33094532028cee2a1929e20e57786f3720baac1a96e50@group.calendar.google.com',

  // Feature flags. A flag that's off can be previewed with ?flag=<name>, e.g. /some-page?flag=someFlag
  features: {},

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
