// Subscribe links for the public "FWP Community Events" Google Calendar (communityCalendarId in app.config.ts).
export function useCommunityCalendar() {
  const { communityCalendarId: id } = useAppConfig() as { communityCalendarId: string }
  const enc = encodeURIComponent(id)
  return {
    // Opens Google Calendar's "Add this calendar?" prompt.
    google: `https://calendar.google.com/calendar/u/0?cid=${btoa(id).replace(/=+$/, '')}`,
    // Subscribes Apple Calendar or Outlook to the public iCal feed.
    ics: `webcal://calendar.google.com/calendar/ical/${enc}/public/basic.ics`,
    // The calendar as a web page, for anyone who just wants to look.
    web: `https://calendar.google.com/calendar/embed?src=${enc}&ctz=America%2FNew_York`,
  }
}
