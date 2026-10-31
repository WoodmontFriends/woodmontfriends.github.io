<script setup lang="ts">
// 3D park explorer: walk or fly around the concept model, or follow the trail loop.
// Assets live in public/explore/ (built in Blender from USGS lidar + OpenStreetMap; see CLAUDE.md).
// Nothing downloads until the visitor presses "Explore in 3D" (the model is about 3.5 MB).
const props = defineProps({
  base: { type: String, default: '/explore/' },
  poster: { type: String, default: '/explore/park-overview.jpg' },
})

type Vec3 = [number, number, number]
type Meta = {
  W: number; H: number; DX: number; DY: number; extW: number; extH: number
  presets: Record<string, { pos: Vec3; look: Vec3 }>
  trail: Vec3[]
}

const status = ref<'idle' | 'loading' | 'ready' | 'error'>('idle')
const progress = ref(0)
const errorText = ref('')
const presetNames = ref<string[]>([])
const mode = ref<'walk' | 'fly'>('fly')
const touring = ref(false)
const treesOn = ref(true)
const tourFeet = ref(0)
const totalFeet = ref(0)
const box = ref<HTMLElement | null>(null)
const canvas = ref<HTMLCanvasElement | null>(null)

// Filled in once the model loads; the template's buttons call these.
let api: {
  goTo: (name: string) => void
  setMode: (m: 'walk' | 'fly') => void
  toggleTour: () => void
  seek: (frac: number) => void
  toggleTrees: () => void
  hold: (v: number) => void
} | null = null
let cleanup: (() => void) | null = null

async function start() {
  if (status.value !== 'idle' && status.value !== 'error') return
  status.value = 'loading'
  progress.value = 0
  try {
    await nextTick()
    await boot()
    status.value = 'ready'
  } catch (err) {
    console.error(err)
    errorText.value = 'The 3D model could not load. Check your connection and try again.'
    status.value = 'error'
  }
}

async function boot() {
  const THREE = await import('three')
  const { GLTFLoader } = await import('three/examples/jsm/loaders/GLTFLoader.js')
  const { DRACOLoader } = await import('three/examples/jsm/loaders/DRACOLoader.js')
  const el = canvas.value!
  const holder = box.value!

  const [meta, hbuf] = await Promise.all([
    fetch(props.base + 'meta.json').then(r => r.json() as Promise<Meta>),
    fetch(props.base + 'height.bin').then(r => r.arrayBuffer()),
  ])
  const HGT = new Int16Array(hbuf)
  function ground(x: number, z: number) {
    const c = (x + meta.extW / 2) / meta.DX - 0.5
    const r = (meta.extH / 2 + z) / meta.DY - 0.5
    const cc = Math.max(0, Math.min(meta.W - 1.001, c))
    const rr = Math.max(0, Math.min(meta.H - 1.001, r))
    const i = Math.floor(rr), j = Math.floor(cc), fr = rr - i, fc = cc - j
    const g = (a: number, b: number) => HGT[a * meta.W + b] / 100
    return g(i, j) * (1 - fr) * (1 - fc) + g(i, j + 1) * (1 - fr) * fc + g(i + 1, j) * fr * (1 - fc) + g(i + 1, j + 1) * fr * fc
  }

  const renderer = new THREE.WebGLRenderer({ canvas: el, antialias: true })
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5))
  const scene = new THREE.Scene()
  const sky = new THREE.Color('#cfe3ef')
  scene.background = sky
  scene.fog = new THREE.Fog(sky, 180, 650)
  const camera = new THREE.PerspectiveCamera(62, 1, 0.2, 3000)
  scene.add(new THREE.HemisphereLight(0xe6f1f8, 0x56633a, 2.2))
  const sun = new THREE.DirectionalLight(0xfff6e6, 2.4)
  sun.position.set(-200, 320, 180)
  scene.add(sun)

  function resize() {
    const w = holder.clientWidth, h = holder.clientHeight
    renderer.setSize(w, h, false)
    camera.aspect = w / h
    camera.updateProjectionMatrix()
  }
  const ro = new ResizeObserver(resize)
  ro.observe(holder)
  resize()

  const draco = new DRACOLoader()
  draco.setDecoderPath(props.base + 'draco/')
  const loader = new GLTFLoader()
  loader.setDRACOLoader(draco)
  const gltf: any = await new Promise((resolve, reject) =>
    loader.load(props.base + 'park.glb', resolve, (e: ProgressEvent) => {
      if (e.total) progress.value = Math.round((e.loaded / e.total) * 100)
    }, reject))
  gltf.scene.traverse((o: any) => {
    if (o.isMesh && o.material?.transparent) o.material.depthWrite = false
  })
  scene.add(gltf.scene)
  let treesNode: any = null
  gltf.scene.traverse((o: any) => { if (!treesNode && /^Trees/.test(o.name)) treesNode = o })

  // ---- camera state ----
  let yaw = 0, pitch = 0
  const pos = new THREE.Vector3()
  const V = (a: Vec3) => new THREE.Vector3(a[0], a[1], a[2])
  function lookAt(p: InstanceType<typeof THREE.Vector3>) {
    const d = new THREE.Vector3().subVectors(p, pos)
    yaw = Math.atan2(-d.x, -d.z)
    pitch = Math.atan2(d.y, Math.hypot(d.x, d.z))
  }
  function apply() {
    camera.position.copy(pos)
    camera.rotation.set(pitch, yaw, 0, 'YXZ')
  }
  const first = meta.presets.Overview ?? Object.values(meta.presets)[0]
  pos.copy(V(first.pos)); lookAt(V(first.look)); apply()
  presetNames.value = Object.keys(meta.presets)

  // ---- trail tour ----
  const T = meta.trail.map(V)
  const segL = [0]
  for (let i = 1; i < T.length; i++) segL.push(segL[i - 1] + T[i].distanceTo(T[i - 1]))
  const total = segL[segL.length - 1]
  totalFeet.value = Math.round(total * 3.281)
  let tourD = 0
  function at(d: number) {
    d = Math.max(0, Math.min(total, d))
    let i = 1
    while (i < segL.length - 1 && segL[i] < d) i++
    const t = (d - segL[i - 1]) / ((segL[i] - segL[i - 1]) || 1)
    return T[i - 1].clone().lerp(T[i], t)
  }
  const showProgress = () => { tourFeet.value = Math.round(tourD * 3.281) }

  // ---- animated moves between viewpoints ----
  let move: null | { t: number; from: any; to: any; fy: number; dy: number; fp: number; tp: number } = null
  function setMode(m: 'walk' | 'fly') {
    mode.value = m
    if (m === 'walk') { pos.y = ground(pos.x, pos.z) + 1.7; pitch = Math.max(-0.6, Math.min(0.6, pitch)) }
  }
  function stopTour() { touring.value = false }

  // ---- input (keys only while the explorer has focus, so the page still scrolls normally) ----
  const keys = new Set<string>()
  let drag: null | { x: number; y: number; id: number } = null
  let hold = 0
  const MOVE_KEYS = ['w', 'a', 's', 'd', 'r', 'f', 'arrowup', 'arrowdown', 'arrowleft', 'arrowright']
  const onKeyDown = (e: KeyboardEvent) => {
    const k = e.key.toLowerCase()
    if ((e.target as HTMLElement)?.tagName === 'BUTTON' && (k === ' ' || k === 'enter')) return
    if (MOVE_KEYS.includes(k)) { e.preventDefault(); stopTour(); move = null }
    keys.add(k)
  }
  const onKeyUp = (e: KeyboardEvent) => keys.delete(e.key.toLowerCase())
  const onBlur = () => keys.clear()
  const onDown = (e: PointerEvent) => { drag = { x: e.clientX, y: e.clientY, id: e.pointerId }; el.setPointerCapture(e.pointerId); move = null; el.focus() }
  const onMove = (e: PointerEvent) => {
    if (!drag || drag.id !== e.pointerId) return
    const k = 0.0042
    yaw -= (e.clientX - drag.x) * k
    pitch = Math.max(-1.45, Math.min(1.45, pitch - (e.clientY - drag.y) * k))
    drag.x = e.clientX; drag.y = e.clientY
  }
  const onUp = (e: PointerEvent) => { if (drag?.id === e.pointerId) drag = null }
  holder.addEventListener('keydown', onKeyDown)
  holder.addEventListener('keyup', onKeyUp)
  holder.addEventListener('focusout', onBlur)
  el.addEventListener('pointerdown', onDown)
  el.addEventListener('pointermove', onMove)
  el.addEventListener('pointerup', onUp)
  el.addEventListener('pointercancel', onUp)

  // ---- loop ----
  const clock = new THREE.Clock()
  let raf = 0
  function frame() {
    const dt = Math.min(clock.getDelta(), 0.1)
    if (move) {
      move.t += dt / 1.4
      const e = move.t >= 1 ? 1 : move.t * move.t * (3 - 2 * move.t)
      pos.lerpVectors(move.from, move.to, e)
      yaw = move.fy + move.dy * e
      pitch = move.fp + (move.tp - move.fp) * e
      if (move.t >= 1) move = null
    } else if (touring.value) {
      tourD += dt * 7
      if (tourD >= total) { tourD = total; stopTour() }
      const p = at(tourD), a = at(tourD + 16)
      a.y -= 2
      pos.copy(p)
      const d = new THREE.Vector3().subVectors(a, pos)
      const ty = Math.atan2(-d.x, -d.z), tp = Math.atan2(d.y, Math.hypot(d.x, d.z))
      yaw += Math.atan2(Math.sin(ty - yaw), Math.cos(ty - yaw)) * Math.min(1, dt * 3)
      pitch += (tp - pitch) * Math.min(1, dt * 3)
      showProgress()
    } else {
      const fast = keys.has('shift') ? 3 : 1
      const sp = (mode.value === 'walk' ? 4 : 16) * fast * dt
      const fwd = mode.value === 'fly'
        ? new THREE.Vector3(-Math.sin(yaw) * Math.cos(pitch), Math.sin(pitch), -Math.cos(yaw) * Math.cos(pitch))
        : new THREE.Vector3(-Math.sin(yaw), 0, -Math.cos(yaw))
      const right = new THREE.Vector3(Math.cos(yaw), 0, -Math.sin(yaw))
      let f = hold
      if (keys.has('w') || keys.has('arrowup')) f += 1
      if (keys.has('s') || keys.has('arrowdown')) f -= 1
      let s = 0
      if (keys.has('d') || keys.has('arrowright')) s += 1
      if (keys.has('a') || keys.has('arrowleft')) s -= 1
      pos.addScaledVector(fwd, f * sp).addScaledVector(right, s * sp)
      if (mode.value === 'fly') { if (keys.has('r')) pos.y += sp; if (keys.has('f')) pos.y -= sp }
      const hx = meta.extW / 2 - 5, hz = meta.extH / 2 - 5
      pos.x = Math.max(-hx, Math.min(hx, pos.x))
      pos.z = Math.max(-hz, Math.min(hz, pos.z))
      const gy = ground(pos.x, pos.z)
      if (mode.value === 'walk') pos.y += (gy + 1.7 - pos.y) * Math.min(1, dt * 10)
      else pos.y = Math.max(pos.y, gy + 1.2)
    }
    apply()
    renderer.render(scene, camera)
    raf = requestAnimationFrame(frame)
  }
  frame()

  api = {
    goTo(name) {
      const p = meta.presets[name]
      if (!p) return
      stopTour()
      setMode(name === 'Trailhead' ? 'walk' : 'fly')
      const from = pos.clone(), fy = yaw, fp = pitch, to = V(p.pos)
      pos.copy(to); lookAt(V(p.look))
      const ty = yaw, tp = pitch
      pos.copy(from); yaw = fy; pitch = fp
      move = { t: 0, from, to, fy, dy: Math.atan2(Math.sin(ty - fy), Math.cos(ty - fy)), fp, tp }
    },
    setMode(m) { stopTour(); setMode(m) },
    toggleTour() {
      if (touring.value) { stopTour(); return }
      move = null; setMode('fly')
      if (tourD >= total - 1) tourD = 0
      touring.value = true
    },
    seek(frac) {
      tourD = total * Math.max(0, Math.min(1, frac))
      const p = at(tourD), a = at(tourD + 16)
      a.y -= 2
      pos.copy(p); lookAt(a); setMode('fly'); showProgress()
    },
    toggleTrees() {
      if (!treesNode) return
      treesNode.visible = !treesNode.visible
      treesOn.value = treesNode.visible
    },
    hold(v) { hold = v; if (v) { stopTour(); move = null } },
  }

  cleanup = () => {
    cancelAnimationFrame(raf)
    ro.disconnect()
    holder.removeEventListener('keydown', onKeyDown)
    holder.removeEventListener('keyup', onKeyUp)
    holder.removeEventListener('focusout', onBlur)
    el.removeEventListener('pointerdown', onDown)
    el.removeEventListener('pointermove', onMove)
    el.removeEventListener('pointerup', onUp)
    el.removeEventListener('pointercancel', onUp)
    draco.dispose()
    renderer.dispose()
  }
}

function pickPreset(e: Event) {
  const el = e.target as HTMLSelectElement
  if (el.value) api?.goTo(el.value)
  el.value = ''
}
function seekFromClick(e: MouseEvent) {
  const r = (e.currentTarget as HTMLElement).getBoundingClientRect()
  api?.seek((e.clientX - r.left) / r.width)
}
async function fullscreen() {
  try {
    if (document.fullscreenElement) await document.exitFullscreen()
    else await box.value?.requestFullscreen()
  } catch {
    // Some phones don't allow fullscreen; the explorer still works in the page.
  }
}

onBeforeUnmount(() => cleanup?.())
</script>

<template>
  <div ref="box" class="explorer" tabindex="-1" aria-label="3D model of Woodmont Park">
    <canvas v-show="status === 'ready'" ref="canvas" class="view" tabindex="0" aria-label="3D view. Drag to look around; with focus, W A S D keys move." />

    <div v-if="status !== 'ready'" class="cover" :style="{ backgroundImage: `url(${poster})` }">
      <div class="cover-card">
        <template v-if="status === 'loading'">
          <p class="cover-title">Loading the park…</p>
          <p class="cover-note">{{ progress }}%</p>
        </template>
        <template v-else>
          <p class="cover-title">Walk the park in 3D</p>
          <p class="cover-note">Fly over the woods, follow the trail, or look around the courts. About a 3.5 MB download.</p>
          <p v-if="status === 'error'" class="cover-error">{{ errorText }}</p>
          <button type="button" class="btn-blaze" @click="start">{{ status === 'error' ? 'Try again' : 'Explore in 3D' }}</button>
        </template>
      </div>
    </div>

    <template v-if="status === 'ready'">
      <div class="help">
        <span>Drag to look</span>
        <span class="keys">· <kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> to move · <kbd>Shift</kbd> faster · <kbd>R</kbd>/<kbd>F</kbd> up and down</span>
      </div>
      <div class="dock">
        <div class="panel" role="group" aria-label="Viewpoints">
          <span class="label">Go to</span>
          <button v-for="n in presetNames" :key="n" type="button" class="preset-btn" @click="api?.goTo(n)">{{ n }}</button>
          <select class="preset-select" aria-label="Go to a viewpoint" @change="pickPreset">
            <option value="">Go to…</option>
            <option v-for="n in presetNames" :key="n" :value="n">{{ n }}</option>
          </select>
        </div>
        <div class="panel grow">
          <button type="button" class="btn-blaze small" @click="api?.toggleTour()">{{ touring ? 'Pause' : 'Follow the trail' }}</button>
          <div class="progress">
            <div class="bar" title="Jump along the trail" @click="seekFromClick"><i :style="{ width: totalFeet ? `${(tourFeet / totalFeet) * 100}%` : '0%' }" /></div>
            <span class="feet">{{ tourFeet.toLocaleString() }} of {{ totalFeet.toLocaleString() }} ft</span>
          </div>
        </div>
        <div class="panel" role="group" aria-label="Movement">
          <button type="button" :aria-pressed="mode === 'walk'" @click="api?.setMode('walk')">Walk</button>
          <button type="button" :aria-pressed="mode === 'fly'" @click="api?.setMode('fly')">Fly</button>
          <button type="button" :aria-pressed="treesOn" @click="api?.toggleTrees()">Trees</button>
          <span class="touchpad">
            <button type="button" aria-label="Move forward" @pointerdown.prevent="api?.hold(1)" @pointerup="api?.hold(0)" @pointerleave="api?.hold(0)" @pointercancel="api?.hold(0)">▲</button>
            <button type="button" aria-label="Move back" @pointerdown.prevent="api?.hold(-1)" @pointerup="api?.hold(0)" @pointerleave="api?.hold(0)" @pointercancel="api?.hold(0)">▼</button>
          </span>
          <button type="button" class="fs-btn" aria-label="Full screen" @click="fullscreen">
            <span class="fs-text">Full screen</span>
            <svg class="fs-icon" viewBox="0 0 20 20" aria-hidden="true"><path d="M3 8V3h5M12 3h5v5M17 12v5h-5M8 17H3v-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" /></svg>
          </button>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.explorer {
  position: relative;
  height: min(78vh, 720px);
  min-height: 420px;
  border-radius: 12px;
  overflow: hidden;
  background: #cfe3ef;
  color: var(--on-dark);
}
.explorer:fullscreen {
  height: 100%;
  border-radius: 0;
}
.view {
  display: block;
  width: 100%;
  height: 100%;
  touch-action: none;
  cursor: grab;
}
.view:active {
  cursor: grabbing;
}
.cover {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  background-size: cover;
  background-position: center;
  padding: 1rem;
}
.cover-card {
  background: var(--hemlock);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  max-width: 26rem;
  text-align: center;
  box-shadow: 0 10px 30px rgba(22, 43, 34, 0.35);
}
.cover-title {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 1.5rem;
  margin: 0 0 0.35rem;
  color: var(--on-dark);
}
.cover-note {
  margin: 0 0 1rem;
  color: var(--on-dark-soft);
  font-size: 0.95rem;
}
.cover-error {
  margin: 0 0 1rem;
  color: var(--blaze);
  font-size: 0.95rem;
}
button {
  font: 500 0.85rem/1 var(--font-body);
  color: var(--on-dark);
  background: #2b4d3d;
  border: 1px solid rgba(233, 240, 234, 0.18);
  border-radius: 8px;
  padding: 0.55rem 0.75rem;
  cursor: pointer;
}
button:hover {
  border-color: rgba(242, 194, 48, 0.6);
}
button:focus-visible {
  outline: 2px solid var(--blaze);
  outline-offset: 2px;
}
button[aria-pressed='true'] {
  background: var(--fern);
  color: var(--hemlock);
  border-color: var(--fern);
}
.btn-blaze {
  background: var(--blaze);
  color: var(--ink);
  border-color: var(--blaze);
  font-weight: 600;
  font-size: 1rem;
  padding: 0.75rem 1.25rem;
}
.btn-blaze:hover {
  background: var(--blaze-hover);
}
.btn-blaze.small {
  font-size: 0.85rem;
  padding: 0.55rem 0.85rem;
}
.help {
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
  background: rgba(31, 58, 46, 0.88);
  border-radius: 8px;
  padding: 0.4rem 0.7rem;
  font-size: 0.8rem;
  max-width: calc(100% - 1.5rem);
}
kbd {
  font: 600 0.72rem var(--font-body);
  background: #2b4d3d;
  border: 1px solid rgba(233, 240, 234, 0.18);
  border-radius: 4px;
  padding: 0 0.3rem;
  margin: 0 0.05rem;
}
.dock {
  position: absolute;
  left: 0.75rem;
  right: 0.75rem;
  bottom: 0.75rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  pointer-events: none;
}
.panel {
  pointer-events: auto;
  background: var(--hemlock);
  border-radius: 10px;
  padding: 0.4rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  align-items: center;
  min-width: 0;
  box-shadow: 0 6px 20px rgba(22, 43, 34, 0.25);
}
.panel.grow {
  flex: 1 1 18rem;
}
.label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--on-dark-soft);
  padding: 0 0.35rem;
}
.progress {
  flex: 1 1 8rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.78rem;
  font-variant-numeric: tabular-nums;
  min-width: 0;
}
.bar {
  flex: 1;
  height: 6px;
  border-radius: 3px;
  background: #2b4d3d;
  overflow: hidden;
  cursor: pointer;
}
.bar i {
  display: block;
  height: 100%;
  background: var(--blaze);
}
.feet {
  white-space: nowrap;
}
.touchpad {
  display: none;
  gap: 0.35rem;
}
.fs-icon {
  display: none;
  width: 1rem;
  height: 1rem;
}
.preset-select {
  display: none;
  font: 500 0.85rem var(--font-body);
  color: var(--on-dark);
  background: #2b4d3d;
  border: 1px solid rgba(233, 240, 234, 0.18);
  border-radius: 8px;
  padding: 0 0.5rem;
  min-height: 2.5rem;
}
@media (hover: none) {
  .touchpad {
    display: flex;
  }
  .keys {
    display: none;
  }
  button {
    min-height: 2.5rem;
  }
  .touchpad button {
    min-width: 2.75rem;
  }
}
/* Phones: one picker for viewpoints and two short rows of controls, so the view stays open. */
@media (max-width: 640px) {
  .explorer {
    height: 82vh;
    height: 82svh;
    min-height: 380px;
  }
  .help {
    display: none;
  }
  .dock {
    left: 0.5rem;
    right: 0.5rem;
    bottom: 0.5rem;
    gap: 0.35rem;
  }
  .panel {
    padding: 0.3rem;
    gap: 0.3rem;
  }
  .label,
  .preset-btn {
    display: none;
  }
  .preset-select {
    display: block;
  }
  .panel.grow {
    flex: 1 1 12rem;
  }
  .progress {
    flex: 1 1 3rem;
  }
  .feet,
  .fs-text {
    display: none;
  }
  .fs-icon {
    display: block;
  }
  button {
    padding: 0.5rem 0.6rem;
  }
  .fs-btn,
  .touchpad button {
    min-width: 2.5rem;
    display: grid;
    place-items: center;
  }
}
</style>
