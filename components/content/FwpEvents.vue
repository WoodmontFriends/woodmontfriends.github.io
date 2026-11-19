<script setup lang="ts">
// Upcoming community events from the public "FWP Community Events" Google Calendar, read in the
// browser from admin.woodmontfriends.org/api/public/events (fwp-admin lib/public-calendar.ts).
// The calendar is the only source of events: nothing here is dated in the build, and any event whose
// last day has passed (Eastern time) is dropped in the browser too, so the page can't go stale.
//
// The admin app scales to zero, so a first request can take several seconds: a skeleton shows while
// it loads, the last good list (kept in this browser) shows straight away on repeat visits, and the
// request gives up after FETCH_TIMEOUT_MS.
//
// `bare` renders only the list, for use inside a ::page-section (home page); otherwise it's a whole
// band with its own heading (/projects). The default slot is the text shown when nothing is coming up.
interface PublicEvent {
  id: string
  title: string
  date: string // YYYY-MM-DD (ET)
  time: string // HH:MM (ET), '' for all-day
  endDate: string // last day, inclusive
  location: string
}
interface Feed {
  enabled: boolean
  events: PublicEvent[]
  error?: string
}

const props = defineProps({
  title: { type: String, default: 'Upcoming events' },
  intro: { type: String, default: '' },
  limit: { type: Number, default: 6 },
  bare: { type: Boolean, default: false },
})

const FETCH_TIMEOUT_MS = 15_000
const CACHE_KEY = 'fwp-events-v1'
const CACHE_MAX_AGE_MS = 7 * 24 * 60 * 60_000

const { publicEventsUrl } = useAppConfig() as { publicEventsUrl: string }
const calendar = useCommunityCalendar()
const all = ref<PublicEvent[]>([])
const state = ref<'loading' | 'ready' | 'error'>('loading')

// Today in Eastern time as YYYY-MM-DD, the same calendar the feed's dates use.
const todayET = () => new Intl.DateTimeFormat('en-CA', { timeZone: 'America/New_York' }).format(new Date())
const upcoming = (list: PublicEvent[]) => {
  const today = todayET()
  return list.filter((e) => /^\d{4}-\d{2}-\d{2}$/.test(e.date) && (e.endDate || e.date) >= today)
}
const events = computed(() => upcoming(all.value).slice(0, props.limit))

const day = (d: string) => new Date(`${d}T12:00:00`)
const month = (d: string) => day(d).toLocaleDateString('en-US', { month: 'short' })
const dayNum = (d: string) => String(day(d).getDate())
function when(e: PublicEvent) {
  const opts: Intl.DateTimeFormatOptions = { weekday: 'long', month: 'long', day: 'numeric' }
  let s = day(e.date).toLocaleDateString('en-US', opts)
  if (e.endDate && e.endDate !== e.date) s += ` to ${day(e.endDate).toLocaleDateString('en-US', opts)}`
  if (e.time) {
    const [h, m] = e.time.split(':').map(Number)
    s += `, ${new Date(2000, 0, 1, h, m).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })}`
  }
  return s
}

function readCache(): PublicEvent[] | null {
  try {
    const c = JSON.parse(localStorage.getItem(CACHE_KEY) || 'null') as { at: number; events: PublicEvent[] } | null
    return c && Date.now() - c.at < CACHE_MAX_AGE_MS && Array.isArray(c.events) ? c.events : null
  } catch {
    return null
  }
}
function writeCache(list: PublicEvent[]) {
  try {
    localStorage.setItem(CACHE_KEY, JSON.stringify({ at: Date.now(), events: list }))
  } catch {
    // Private windows and blocked storage: the page works without the cache.
  }
}

onMounted(async () => {
  const cached = readCache()
  if (cached) {
    all.value = cached
    state.value = 'ready'
  }
  const ctrl = new AbortController()
  const timer = setTimeout(() => ctrl.abort(), FETCH_TIMEOUT_MS)
  try {
    const res = await fetch(publicEventsUrl, { headers: { accept: 'application/json' }, signal: ctrl.signal })
    if (!res.ok) throw new Error(String(res.status))
    const feed = (await res.json()) as Feed
    if (feed.enabled && feed.error) throw new Error(feed.error)
    all.value = feed.enabled && Array.isArray(feed.events) ? feed.events : []
    writeCache(all.value)
    state.value = 'ready'
  } catch {
    // Keep a cached list if there is one (already date-filtered); otherwise say so and link the calendar.
    if (!cached) state.value = 'error'
  } finally {
    clearTimeout(timer)
  }
})
</script>

<template>
  <component :is="bare ? 'div' : 'section'" :id="bare ? undefined : 'events'" :class="bare ? 'bare' : 'band'" :aria-labelledby="bare ? undefined : 'events-title'">
   <div :class="{ wrap: !bare }">
    <h2 v-if="!bare" id="events-title" class="band-title">{{ title }}</h2>
    <p v-if="intro" class="intro">{{ intro }}</p>
    <div aria-live="polite" :aria-busy="state === 'loading'">
      <ul v-if="state === 'loading'" class="events" aria-label="Loading events">
        <li v-for="n in 2" :key="n" class="event">
          <div class="date skeleton" />
          <div class="details">
            <div class="line skeleton" />
            <div class="line short skeleton" />
          </div>
        </li>
      </ul>
      <p v-else-if="state === 'error'" class="note">
        We couldn't load our events just now.
        <a :href="calendar.web" target="_blank" rel="noopener noreferrer">See our calendar</a> for what's coming up.
      </p>
      <p v-else-if="!events.length" class="note">
        <ContentSlot v-if="$slots.default" :use="$slots.default" unwrap="p" />
        <template v-else>Nothing is on the calendar right now. Check back soon!</template>
      </p>
      <ul v-else class="events">
        <li v-for="e in events" :key="e.id" class="event">
          <div class="date" aria-hidden="true">
            <span class="month">{{ month(e.date) }}</span>
            <span class="day">{{ dayNum(e.date) }}</span>
          </div>
          <div class="details">
            <h3 class="event-title">{{ e.title }}</h3>
            <p class="when">{{ when(e) }}</p>
            <p v-if="e.location" class="where">{{ e.location }}</p>
          </div>
        </li>
      </ul>
    </div>
    <p v-if="!bare" class="subscribe">
      Add our events to your calendar:
      <a :href="calendar.google" target="_blank" rel="noopener noreferrer">Google Calendar</a>
      ·
      <a :href="calendar.ics">Apple or Outlook</a>
      ·
      <a :href="calendar.web" target="_blank" rel="noopener noreferrer">View the full calendar</a>
    </p>
   </div>
  </component>
</template>

<style scoped>
.band {
  background: var(--fern);
  padding: clamp(3rem, 7vw, 5rem) 0;
  scroll-margin-top: 1rem;
}
.bare {
  margin: 2rem 0 0;
}
.band-title {
  font-size: clamp(1.85rem, 4vw, 2.5rem);
  font-weight: 700;
  margin: 0 0 1.25rem;
}
.intro {
  max-width: var(--measure);
  margin: 0 0 1.75rem;
}
.events {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 1.5rem;
}
@media (min-width: 760px) {
  .events {
    grid-template-columns: 1fr 1fr;
    gap: 2rem 3rem;
  }
}
.event {
  display: flex;
  gap: 1.25rem;
  align-items: flex-start;
}
.details {
  flex: 1;
  min-width: 0;
}
.date {
  flex: none;
  width: 4.75rem;
  text-align: center;
  background: var(--hemlock);
  color: var(--on-dark);
  border-radius: 4px;
  padding: 0.55rem 0 0.65rem;
  border-top: 6px solid var(--blaze);
}
.month {
  display: block;
  font-weight: 700;
  font-size: 0.95rem;
}
.day {
  display: block;
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 2rem;
  line-height: 1.1;
}
.event-title {
  font-weight: 700;
  font-size: 1.3rem;
  margin: 0.1rem 0 0.25rem;
}
.when,
.where {
  margin: 0;
  color: var(--ink-soft);
}
.when {
  font-weight: 600;
}
.subscribe {
  margin: 1.75rem 0 0;
  color: var(--ink-soft);
}
.note {
  margin: 0;
  max-width: var(--measure);
  color: var(--ink-soft);
}
.skeleton {
  background: linear-gradient(90deg, var(--rule), #f6f9f5, var(--rule));
  background-size: 200% 100%;
  animation: shimmer 1.4s ease-in-out infinite;
  border: 0;
  border-radius: 4px;
}
.date.skeleton {
  height: 4.6rem;
}
.line {
  height: 1.2rem;
  margin: 0.35rem 0 0.6rem;
  max-width: 16rem;
}
.line.short {
  max-width: 10rem;
}
@keyframes shimmer {
  to {
    background-position: -200% 0;
  }
}
@media (prefers-reduced-motion: reduce) {
  .skeleton {
    animation: none;
  }
}
</style>
