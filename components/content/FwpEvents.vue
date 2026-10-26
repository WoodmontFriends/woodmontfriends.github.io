<script setup lang="ts">
// Upcoming community events from the public "FWP Community Events" calendar, read in the browser
// from admin.woodmontfriends.org/api/public/events. Renders nothing until that calendar is set up.
interface PublicEvent {
  id: string
  title: string
  date: string // YYYY-MM-DD
  time: string // HH:MM, '' for all-day
  endDate: string
  location: string
}
interface Feed {
  enabled: boolean
  links?: { google: string; ics: string; web: string }
  events: PublicEvent[]
  error?: string
}

const props = defineProps({
  title: { type: String, default: 'Upcoming events' },
  intro: { type: String, default: '' },
  limit: { type: Number, default: 6 },
})
const { publicEventsUrl } = useAppConfig() as { publicEventsUrl: string }
const feed = ref<Feed | null>(null)
const failed = ref(false)

const events = computed(() => (feed.value?.events ?? []).slice(0, props.limit))

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

onMounted(async () => {
  try {
    const res = await fetch(publicEventsUrl, { headers: { accept: 'application/json' } })
    if (!res.ok) throw new Error(String(res.status))
    feed.value = (await res.json()) as Feed
  } catch {
    failed.value = true
  }
})
</script>

<template>
  <!-- The whole band, heading included, stays hidden until the public calendar is set up. -->
  <section v-if="feed?.enabled" id="events" class="band" aria-labelledby="events-title">
   <div class="wrap">
    <h2 id="events-title" class="band-title">{{ title }}</h2>
    <p v-if="intro" class="intro">{{ intro }}</p>
    <p v-if="!events.length" class="note">
      {{ feed.error ? "We couldn't load our calendar just now. Please check back soon." : 'Nothing on the calendar yet. Check back soon!' }}
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
    <p v-if="feed.links" class="subscribe">
      Add our events to your calendar:
      <a :href="feed.links.google" target="_blank" rel="noopener noreferrer">Google Calendar</a>
      ·
      <a :href="feed.links.ics.replace(/^https:/, 'webcal:')">Apple or Outlook</a>
      ·
      <a :href="feed.links.web" target="_blank" rel="noopener noreferrer">View the full calendar</a>
    </p>
   </div>
  </section>
</template>

<style scoped>
.band {
  background: var(--fern);
  padding: clamp(3rem, 7vw, 5rem) 0;
  scroll-margin-top: 1rem;
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
  color: var(--ink-soft);
}
</style>
