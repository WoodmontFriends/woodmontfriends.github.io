<script setup lang="ts">
// Park nature map: plant, fungus, and wildlife sightings pulled live from iNaturalist.
// Settings live under `nature` in app.config.ts.
import 'leaflet/dist/leaflet.css'

type Bounds = { swlat: number; swlng: number; nelat: number; nelng: number }
type NatureConfig = {
  projectSlug: string
  bounds: Bounds
  center: [number, number]
  zoom: number
  protectedGenera: string[]
}

type Sighting = {
  id: number
  url: string
  date: string // YYYY-MM-DD
  month: number // months since year 0, for the timeline
  lat: number | null
  lng: number | null
  group: string
  name: string
  sci: string
  photo: string | null
  observer: string
  researchGrade: boolean
  hidden: boolean // location withheld by iNaturalist (sensitive species or observer's choice)
  foraged: boolean // edible species we only show as an area
}

const { nature } = useAppConfig() as { nature: NatureConfig }

// Categorical colors, one per group, in a fixed order (validated for color-vision deficiency).
const GROUPS = [
  { id: 'birds', label: 'Birds', color: '#2a78d6', taxa: ['Aves'] },
  { id: 'fungi', label: 'Fungi', color: '#eb6834', taxa: ['Fungi', 'Protozoa'] },
  { id: 'herps', label: 'Reptiles & amphibians', color: '#1baf7a', taxa: ['Reptilia', 'Amphibia'] },
  { id: 'insects', label: 'Insects & spiders', color: '#eda100', taxa: ['Insecta', 'Arachnida'] },
  { id: 'mammals', label: 'Mammals', color: '#e87ba4', taxa: ['Mammalia'] },
  { id: 'plants', label: 'Plants', color: '#008300', taxa: ['Plantae'] },
  { id: 'other', label: 'Other', color: '#6250d6', taxa: [] as string[] },
]
const groupById = Object.fromEntries(GROUPS.map(g => [g.id, g]))
function groupFor(iconic?: string) {
  return GROUPS.find(g => iconic && g.taxa.includes(iconic))?.id ?? 'other'
}

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
const monthIndex = (d: string) => Number(d.slice(0, 4)) * 12 + Number(d.slice(5, 7)) - 1
const monthLabel = (m: number) => `${MONTHS[m % 12]} ${Math.floor(m / 12)}`
const TRAIL_MONTHS = 3 // the timeline shows the chosen month plus the two before it, fading out

// ---------- state ----------
const status = ref<'loading' | 'ready' | 'error'>('loading')
const sightings = ref<Sighting[]>([])
const totalOnINat = ref(0)
const activeGroups = ref<Set<string>>(new Set(GROUPS.map(g => g.id)))
const search = ref('')
const view = ref<'pins' | 'heat'>('pins')
const basemap = ref<'map' | 'aerial'>('map')
const timeline = ref(false)
const timelineMonth = ref(0)
const playing = ref(false)
const selectedId = ref<number | null>(null)

const projectUrl = computed(() =>
  nature.projectSlug ? `https://www.inaturalist.org/projects/${nature.projectSlug}` : null,
)

// ---------- data ----------
async function load() {
  status.value = 'loading'
  try {
    const all: Sighting[] = []
    const base = new URLSearchParams({ per_page: '200', order_by: 'observed_on', order: 'desc', locale: 'en' })
    if (nature.projectSlug) base.set('project_id', nature.projectSlug)
    else Object.entries(nature.bounds).forEach(([k, v]) => base.set(k, String(v)))

    for (let page = 1; page <= 5; page++) {
      base.set('page', String(page))
      const res = await fetch(`https://api.inaturalist.org/v1/observations?${base}`)
      if (!res.ok) throw new Error(`iNaturalist returned ${res.status}`)
      const data = await res.json()
      totalOnINat.value = data.total_results ?? 0
      for (const o of data.results ?? []) {
        const s = toSighting(o)
        if (s) all.push(s)
      }
      if (page * 200 >= totalOnINat.value) break
    }
    sightings.value = all
    const months = all.map(s => s.month)
    timelineMonth.value = months.length ? Math.max(...months) : 0
    status.value = 'ready'
  } catch (err) {
    console.error('[nature-map]', err)
    status.value = 'error'
  }
}

function toSighting(o: any): Sighting | null {
  const date: string | undefined = o.observed_on || o.time_observed_at?.slice(0, 10)
  if (!date) return null
  const coords = o.geojson?.coordinates
  const sci: string = o.taxon?.name ?? ''
  const genus = sci.split(' ')[0]
  const hidden = Boolean(o.obscured || o.geoprivacy === 'private' || o.taxon_geoprivacy === 'private' || !coords)
  return {
    id: o.id,
    url: o.uri || `https://www.inaturalist.org/observations/${o.id}`,
    date,
    month: monthIndex(date),
    lat: hidden ? null : coords[1],
    lng: hidden ? null : coords[0],
    group: groupFor(o.taxon?.iconic_taxon_name),
    name: o.taxon?.preferred_common_name || sci || o.species_guess || 'Unidentified',
    sci,
    photo: o.photos?.[0]?.url?.replace('/square.', '/small.') ?? null,
    observer: o.user?.login ?? '',
    researchGrade: o.quality_grade === 'research',
    hidden,
    foraged: nature.protectedGenera.includes(genus),
  }
}

// ---------- filtering ----------
const minMonth = computed(() => Math.min(...sightings.value.map(s => s.month)))
const maxMonth = computed(() => Math.max(...sightings.value.map(s => s.month)))

function matchesSearch(s: Sighting) {
  const q = search.value.trim().toLowerCase()
  return !q || s.name.toLowerCase().includes(q) || s.sci.toLowerCase().includes(q)
}
function inWindow(s: Sighting) {
  if (!timeline.value) return true
  return s.month <= timelineMonth.value && s.month > timelineMonth.value - TRAIL_MONTHS
}

// Everything except the group filter, so the chips can show counts.
const beforeGroups = computed(() => sightings.value.filter(s => matchesSearch(s) && inWindow(s)))
const groupCounts = computed(() => {
  const c: Record<string, number> = {}
  for (const s of beforeGroups.value) c[s.group] = (c[s.group] ?? 0) + 1
  return c
})
const visible = computed(() => beforeGroups.value.filter(s => activeGroups.value.has(s.group)))
const pinned = computed(() => visible.value.filter(s => !s.hidden && !s.foraged))
const foraged = computed(() => visible.value.filter(s => !s.hidden && s.foraged))
const hiddenCount = computed(() => visible.value.filter(s => s.hidden).length)

function toggleGroup(id: string) {
  const next = new Set(activeGroups.value)
  next.has(id) ? next.delete(id) : next.add(id)
  activeGroups.value = next
}
function onlyGroup(id: string) {
  activeGroups.value = new Set([id])
}
function allGroups() {
  activeGroups.value = new Set(GROUPS.map(g => g.id))
}

// ---------- timeline playback ----------
let playTimer: ReturnType<typeof setInterval> | undefined
function togglePlay() {
  if (playing.value) return stopPlay()
  if (timelineMonth.value >= maxMonth.value) timelineMonth.value = minMonth.value
  playing.value = true
  playTimer = setInterval(() => {
    if (timelineMonth.value >= maxMonth.value) return stopPlay()
    timelineMonth.value++
  }, 900)
}
function stopPlay() {
  playing.value = false
  clearInterval(playTimer)
}
watch(timeline, on => { if (!on) stopPlay() })

// ---------- map ----------
const mapEl = ref<HTMLElement | null>(null)
let L: any
let map: any
let tiles: Record<string, any> = {}
let pinLayer: any
let areaLayer: any
let heatLayer: any
const markers = new Map<number, any>()

const HEAT_GRADIENT = { 0.2: '#9ec5f4', 0.45: '#5598e7', 0.7: '#256abf', 1: '#0d366b' }
const AREA_GRID = 0.0015 // ~150 m cells for foraged species

async function initMap() {
  L = (await import('leaflet')).default
  ;(window as any).L = L
  await import('leaflet.heat')
  if (!mapEl.value || map) return // unmounted while loading, or already set up

  const { swlat, swlng, nelat, nelng } = nature.bounds
  map = L.map(mapEl.value!, { zoomControl: true, scrollWheelZoom: false })
    .fitBounds([[swlat, swlng], [nelat, nelng]])
  map.on('focus', () => map.scrollWheelZoom.enable())
  map.on('blur', () => map.scrollWheelZoom.disable())

  tiles.map = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  })
  tiles.aerial = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 19,
    attribution: 'Imagery &copy; Esri, Maxar, Earthstar Geographics',
  })
  tiles[basemap.value].addTo(map)
  map.attributionControl.addAttribution('Sightings from <a href="https://www.inaturalist.org">iNaturalist</a>')

  pinLayer = L.layerGroup().addTo(map)
  areaLayer = L.layerGroup().addTo(map)
  heatLayer = L.heatLayer([], { radius: 28, blur: 22, maxZoom: 18, minOpacity: 0.3, gradient: HEAT_GRADIENT })
  draw()
}

function opacityFor(s: Sighting) {
  if (!timeline.value) return 1
  const age = timelineMonth.value - s.month
  return [1, 0.55, 0.25][age] ?? 0.25
}

function draw() {
  if (!map) return
  pinLayer.clearLayers()
  areaLayer.clearLayers()
  markers.clear()

  if (view.value === 'heat') {
    if (!map.hasLayer(heatLayer)) heatLayer.addTo(map)
    heatLayer.setLatLngs(pinned.value.map(s => [s.lat, s.lng, opacityFor(s)]))
  } else {
    if (map.hasLayer(heatLayer)) map.removeLayer(heatLayer)
    // Oldest first so recent sightings sit on top.
    for (const s of [...pinned.value].reverse()) {
      const g = groupById[s.group]
      const o = opacityFor(s)
      const m = L.circleMarker([s.lat, s.lng], {
        radius: 7,
        color: '#ffffff',
        weight: 2,
        fillColor: g.color,
        fillOpacity: 0.9 * o,
        opacity: o,
      })
        .bindTooltip(`${escapeHtml(s.name)} · ${formatDate(s.date)}`, { direction: 'top', offset: [0, -6] })
        .bindPopup(popupHtml(s), { maxWidth: 240 })
        .on('click', () => { selectedId.value = s.id })
      m.addTo(pinLayer)
      markers.set(s.id, m)
    }
  }

  // Foraged species: one soft circle per ~150 m cell, never an exact point.
  const cells = new Map<string, { lat: number; lng: number; names: Set<string>; n: number }>()
  for (const s of foraged.value) {
    const lat = (Math.floor(s.lat! / AREA_GRID) + 0.5) * AREA_GRID
    const lng = (Math.floor(s.lng! / AREA_GRID) + 0.5) * AREA_GRID
    const key = `${lat},${lng}`
    const cell = cells.get(key) ?? { lat, lng, names: new Set(), n: 0 }
    cell.names.add(s.name)
    cell.n++
    cells.set(key, cell)
  }
  for (const c of cells.values()) {
    L.circle([c.lat, c.lng], {
      radius: 110,
      color: groupById.fungi.color,
      weight: 1.5,
      dashArray: '4 4',
      fillColor: groupById.fungi.color,
      fillOpacity: 0.15,
    })
      .bindTooltip(`${[...c.names].map(escapeHtml).join(', ')} somewhere around here (${c.n})`, { sticky: true })
      .addTo(areaLayer)
  }
}

function popupHtml(s: Sighting) {
  const img = s.photo ? `<img src="${s.photo}" alt="" class="nm-pop-img" loading="lazy">` : ''
  const sci = s.sci && s.sci !== s.name ? `<em>${escapeHtml(s.sci)}</em><br>` : ''
  return `${img}<strong>${escapeHtml(s.name)}</strong><br>${sci}${formatDate(s.date)}${s.observer ? ` · ${escapeHtml(s.observer)}` : ''}<br><a href="${s.url}" target="_blank" rel="noopener noreferrer">View on iNaturalist</a>`
}

function focusSighting(s: Sighting) {
  selectedId.value = s.id
  const m = markers.get(s.id)
  if (m && map) {
    map.setView(m.getLatLng(), Math.max(map.getZoom(), 17))
    m.openPopup()
  }
}

watch([pinned, foraged, view, timelineMonth], draw)
watch(basemap, (b, prev) => {
  if (!map) return
  map.removeLayer(tiles[prev])
  tiles[b].addTo(map)
})

onMounted(() => {
  initMap()
  load()
})
onBeforeUnmount(() => {
  stopPlay()
  map?.remove()
})

// ---------- helpers ----------
function formatDate(d: string) {
  const [y, m, day] = d.split('-').map(Number)
  return `${MONTHS[m - 1]} ${day}, ${y}`
}
function escapeHtml(t: string) {
  return t.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!)
}

const listed = computed(() => visible.value.slice(0, 60))
</script>

<template>
  <section class="nature-map" aria-label="Park nature map">
    <div class="wrap">
      <!-- Filters -->
      <div class="nm-controls">
        <div class="nm-groups" role="group" aria-label="Show these groups">
          <button
            v-for="g in GROUPS"
            :key="g.id"
            type="button"
            class="nm-chip"
            :class="{ off: !activeGroups.has(g.id) }"
            :aria-pressed="activeGroups.has(g.id)"
            :title="`Click to toggle. Double-click to show only ${g.label.toLowerCase()}.`"
            @click="toggleGroup(g.id)"
            @dblclick.prevent="onlyGroup(g.id)"
          >
            <span class="nm-swatch" :style="{ background: g.color }" aria-hidden="true" />
            {{ g.label }}
            <span class="nm-count">{{ groupCounts[g.id] ?? 0 }}</span>
          </button>
          <button v-if="activeGroups.size < GROUPS.length" type="button" class="nm-link" @click="allGroups">Show all</button>
        </div>

        <div class="nm-row">
          <label class="nm-search">
            <span class="sr-only">Search species</span>
            <input v-model="search" type="search" placeholder="Search: puffball, deer, oak…" autocomplete="off">
          </label>
          <div class="nm-seg" role="group" aria-label="Map style">
            <button type="button" :aria-pressed="view === 'pins'" @click="view = 'pins'">Pins</button>
            <button type="button" :aria-pressed="view === 'heat'" @click="view = 'heat'">Heat map</button>
          </div>
          <div class="nm-seg" role="group" aria-label="Background">
            <button type="button" :aria-pressed="basemap === 'map'" @click="basemap = 'map'">Map</button>
            <button type="button" :aria-pressed="basemap === 'aerial'" @click="basemap = 'aerial'">Aerial</button>
          </div>
          <label class="nm-toggle">
            <input v-model="timeline" type="checkbox" :disabled="status !== 'ready' || !sightings.length">
            Timeline
          </label>
        </div>

        <div v-if="timeline && sightings.length" class="nm-timeline">
          <button type="button" class="nm-play" :aria-label="playing ? 'Pause' : 'Play through the months'" @click="togglePlay">
            <svg v-if="!playing" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 2.5v11l9-5.5z" fill="currentColor" /></svg>
            <svg v-else viewBox="0 0 16 16" aria-hidden="true"><path d="M4 2.5h3v11H4zM9 2.5h3v11H9z" fill="currentColor" /></svg>
          </button>
          <input
            v-model.number="timelineMonth"
            type="range"
            :min="minMonth"
            :max="maxMonth"
            step="1"
            aria-label="Month"
            @input="stopPlay"
          >
          <output class="nm-month">{{ monthLabel(timelineMonth) }}</output>
          <p class="nm-hint">Showing this month brightest, with the two months before it fading out, so you can see where things move.</p>
        </div>
      </div>

      <!-- Map + list -->
      <div class="nm-body">
        <div class="nm-map-wrap">
          <div ref="mapEl" class="nm-map" tabindex="0" aria-label="Map of sightings. Focus the map to zoom with the scroll wheel." />
          <div v-if="status === 'loading'" class="nm-overlay">Loading sightings from iNaturalist…</div>
          <div v-else-if="status === 'error'" class="nm-overlay">
            <p>We couldn't reach iNaturalist just now.</p>
            <button type="button" class="btn btn-blaze" @click="load">Try again</button>
          </div>
        </div>

        <aside class="nm-list" aria-label="Recent sightings">
          <div class="nm-list-head">
            <h3>Recent sightings</h3>
            <p v-if="status === 'ready'">
              {{ visible.length.toLocaleString() }} of {{ sightings.length.toLocaleString() }} shown
            </p>
          </div>
          <p v-if="status === 'ready' && !visible.length" class="nm-empty">
            {{ sightings.length ? 'Nothing matches these filters.' : 'No sightings yet. Be the first!' }}
          </p>
          <ul>
            <li v-for="s in listed" :key="s.id">
              <button type="button" class="nm-item" :class="{ selected: selectedId === s.id }" :disabled="s.hidden || s.foraged" @click="focusSighting(s)">
                <img v-if="s.photo" :src="s.photo.replace('/small.', '/square.')" alt="" loading="lazy" width="48" height="48">
                <span v-else class="nm-noimg" aria-hidden="true" />
                <span class="nm-item-text">
                  <span class="nm-item-name">
                    <span class="nm-swatch" :style="{ background: groupById[s.group].color }" aria-hidden="true" />
                    {{ s.name }}
                  </span>
                  <span class="nm-item-meta">
                    {{ formatDate(s.date) }}
                    <template v-if="s.hidden"> · location hidden</template>
                    <template v-else-if="s.foraged"> · rough area only</template>
                  </span>
                </span>
              </button>
              <a class="nm-ext" :href="s.url" target="_blank" rel="noopener noreferrer" :aria-label="`${s.name} on iNaturalist`">↗</a>
            </li>
          </ul>
          <p v-if="visible.length > listed.length" class="nm-more">
            and {{ (visible.length - listed.length).toLocaleString() }} more on the map
          </p>
        </aside>
      </div>

      <p v-if="status === 'ready'" class="nm-notes">
        <template v-if="hiddenCount">
          {{ hiddenCount }} {{ hiddenCount === 1 ? 'sighting is' : 'sightings are' }} left off the map because iNaturalist hides the exact spot to protect a sensitive species or the observer's privacy.
        </template>
        Edible mushrooms like chanterelles show as a dashed circle instead of a pin, so a patch isn't picked clean.
        <template v-if="totalOnINat > sightings.length"> Showing the newest {{ sightings.length.toLocaleString() }} of {{ totalOnINat.toLocaleString() }}.</template>
        <a v-if="projectUrl" :href="projectUrl" target="_blank" rel="noopener noreferrer">See everything on iNaturalist</a>
      </p>
    </div>
  </section>
</template>

<style scoped>
.nature-map {
  padding: 0 0 clamp(2.5rem, 6vw, 4rem);
}
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  white-space: nowrap;
}

.nm-controls {
  display: grid;
  gap: 0.85rem;
  margin-bottom: 1rem;
}
.nm-groups {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}
.nm-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  min-height: 2.4rem;
  padding: 0.35rem 0.8rem;
  border: 1px solid var(--rule);
  border-radius: 999px;
  background: var(--paper);
  color: var(--ink);
  font: 600 0.92rem/1.2 var(--font-body);
  cursor: pointer;
}
.nm-chip:hover {
  border-color: var(--hemlock);
}
.nm-chip.off {
  background: var(--fern);
  color: var(--ink-soft);
}
.nm-chip.off .nm-swatch {
  opacity: 0.3;
}
.nm-count {
  font-weight: 400;
  color: var(--ink-soft);
  font-variant-numeric: tabular-nums;
}
.nm-swatch {
  display: inline-block;
  width: 0.7rem;
  height: 0.7rem;
  border-radius: 50%;
  box-shadow: 0 0 0 2px var(--paper);
  flex: none;
}
.nm-link {
  background: none;
  border: 0;
  padding: 0.4rem;
  color: var(--hemlock);
  font: 600 0.92rem var(--font-body);
  text-decoration: underline;
  cursor: pointer;
}

.nm-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem 1rem;
  align-items: center;
}
.nm-search {
  flex: 1 1 14rem;
  max-width: 22rem;
}
.nm-search input {
  width: 100%;
  min-height: 2.4rem;
  padding: 0.4rem 0.75rem;
  border: 1px solid var(--rule);
  border-radius: 4px;
  font: 1rem var(--font-body);
  color: var(--ink);
}
.nm-search input:focus {
  outline: 3px solid var(--hemlock);
  outline-offset: 1px;
}
.nm-seg {
  display: inline-flex;
  border: 1px solid var(--rule);
  border-radius: 4px;
  overflow: hidden;
}
.nm-seg button {
  min-height: 2.4rem;
  padding: 0.35rem 0.85rem;
  border: 0;
  background: var(--paper);
  color: var(--ink-soft);
  font: 600 0.92rem var(--font-body);
  cursor: pointer;
}
.nm-seg button + button {
  border-left: 1px solid var(--rule);
}
.nm-seg button[aria-pressed='true'] {
  background: var(--hemlock);
  color: var(--on-dark);
}
.nm-toggle {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
}
.nm-toggle input {
  width: 1.1rem;
  height: 1.1rem;
  accent-color: var(--hemlock);
}

.nm-timeline {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  gap: 0.4rem 0.85rem;
  align-items: center;
  padding: 0.75rem 1rem;
  background: var(--fern);
  border-radius: 6px;
}
.nm-play {
  display: grid;
  place-items: center;
  width: 2.4rem;
  height: 2.4rem;
  border: 0;
  border-radius: 50%;
  background: var(--hemlock);
  color: var(--blaze);
  cursor: pointer;
}
.nm-play svg {
  width: 1rem;
  height: 1rem;
}
.nm-timeline input[type='range'] {
  width: 100%;
  accent-color: var(--hemlock);
}
.nm-month {
  min-width: 5.5rem;
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 1.1rem;
  color: var(--hemlock);
  font-variant-numeric: tabular-nums;
}
.nm-hint {
  grid-column: 1 / -1;
  margin: 0;
  font-size: 0.85rem;
  color: var(--ink-soft);
}

.nm-body {
  display: grid;
  gap: 1rem;
}
@media (min-width: 900px) {
  .nm-body {
    grid-template-columns: minmax(0, 1fr) 20rem;
  }
}
.nm-map-wrap {
  position: relative;
  border: 1px solid var(--rule);
  border-radius: 6px;
  overflow: hidden;
}
.nm-map {
  height: clamp(380px, 68vh, 640px);
  background: var(--fern);
}
.nm-overlay {
  position: absolute;
  inset: 0;
  z-index: 500;
  display: grid;
  place-content: center;
  justify-items: center;
  gap: 0.75rem;
  background: rgba(238, 243, 236, 0.85);
  color: var(--hemlock);
  font-weight: 600;
  text-align: center;
}
.nm-overlay p {
  margin: 0;
}

.nm-list {
  display: flex;
  flex-direction: column;
  max-height: clamp(380px, 68vh, 640px);
  border: 1px solid var(--rule);
  border-radius: 6px;
  overflow: hidden;
}
.nm-list-head {
  padding: 0.75rem 1rem 0.6rem;
  border-bottom: 1px solid var(--rule);
}
.nm-list-head h3 {
  margin: 0;
  font-size: 1.15rem;
}
.nm-list-head p {
  margin: 0.1rem 0 0;
  font-size: 0.85rem;
  color: var(--ink-soft);
}
.nm-list ul {
  list-style: none;
  margin: 0;
  padding: 0;
  overflow-y: auto;
}
.nm-list li {
  display: flex;
  align-items: stretch;
  border-bottom: 1px solid var(--rule);
}
.nm-item {
  flex: 1;
  display: flex;
  gap: 0.7rem;
  align-items: center;
  min-width: 0;
  padding: 0.55rem 0.5rem 0.55rem 1rem;
  border: 0;
  background: none;
  text-align: left;
  font: inherit;
  color: inherit;
  cursor: pointer;
}
.nm-item:disabled {
  cursor: default;
}
.nm-item:not(:disabled):hover,
.nm-item.selected {
  background: var(--fern);
}
.nm-item img,
.nm-noimg {
  width: 48px;
  height: 48px;
  border-radius: 4px;
  object-fit: cover;
  flex: none;
  background: var(--fern);
}
.nm-item-text {
  display: grid;
  min-width: 0;
}
.nm-item-name {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-weight: 600;
  font-size: 0.95rem;
  line-height: 1.3;
}
.nm-item-meta {
  font-size: 0.82rem;
  color: var(--ink-soft);
}
.nm-ext {
  display: grid;
  place-items: center;
  width: 2.5rem;
  flex: none;
  color: var(--ink-soft);
  text-decoration: none;
}
.nm-ext:hover {
  color: var(--hemlock);
  background: var(--fern);
}
.nm-empty,
.nm-more {
  margin: 0;
  padding: 1rem;
  font-size: 0.9rem;
  color: var(--ink-soft);
}
.nm-notes {
  margin: 1rem 0 0;
  max-width: 48rem;
  font-size: 0.88rem;
  color: var(--ink-soft);
}

:deep(.nm-pop-img) {
  display: block;
  width: 100%;
  max-height: 160px;
  object-fit: cover;
  margin-bottom: 0.4rem;
  border-radius: 3px;
}
:deep(.leaflet-container) {
  font-family: var(--font-body);
}
</style>
