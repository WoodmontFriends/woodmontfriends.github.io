<script setup lang="ts">
const props = defineProps({
  primaryLabel: { type: String, default: '' },
  primaryHref: { type: String, default: '' },
  secondaryLabel: { type: String, default: '' },
  secondaryHref: { type: String, default: '' },
  // Optional quiet text link under the buttons, e.g. to the calendar call-out (#calendar).
  linkLabel: { type: String, default: '' },
  linkHref: { type: String, default: '' },
  // Optional photo beside the text on wide screens (below it on phones). Path in public/.
  image: { type: String, default: '' },
  imageAlt: { type: String, default: '' },
  imageCaption: { type: String, default: '' },
})
// "signup" resolves to the sign-up form URL in app.config.ts
const { signupUrl } = useAppConfig()
const resolve = (href?: string) => (href === 'signup' ? signupUrl : href || '')
const primary = computed(() => resolve(props.primaryHref))
const secondary = computed(() => resolve(props.secondaryHref))
const isExternal = (href?: string) => Boolean(href && (href === signupUrl || href.startsWith('http://') || href.startsWith('https://')))
</script>

<template>
  <section class="hero on-dark">
    <div class="wrap hero-grid" :class="{ 'has-image': image }">
      <div class="hero-text">
      <h1 class="lockup">
        <span class="lockup-small">Friends of</span>
        <span class="lockup-big">Woodmont Park</span>
      </h1>
      <div class="tagline"><ContentSlot :use="$slots.default" /></div>
      <div v-if="primaryLabel || secondaryLabel" class="actions">
        <a 
          v-if="primaryLabel" 
          :href="primary" 
          :target="isExternal(primary) ? '_blank' : undefined"
          :rel="isExternal(primary) ? 'noopener noreferrer' : undefined"
          class="btn btn-blaze"
        >{{ primaryLabel }}</a>
        <a 
          v-if="secondaryLabel" 
          :href="secondary" 
          :target="isExternal(secondary) ? '_blank' : undefined"
          :rel="isExternal(secondary) ? 'noopener noreferrer' : undefined"
          class="btn btn-ghost"
        >{{ secondaryLabel }}</a>
      </div>
      <p v-if="linkLabel && linkHref" class="hero-link">
        <a :href="linkHref">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <rect x="3" y="4.5" width="18" height="16.5" rx="2" />
            <path d="M3 9.5h18M8 2.5v4M16 2.5v4" />
          </svg>
          {{ linkLabel }}
        </a>
      </p>
      </div>
      <figure v-if="image" class="hero-photo">
        <img :src="image" :alt="imageAlt" width="1024" height="768" fetchpriority="high" />
        <figcaption v-if="imageCaption">{{ imageCaption }}</figcaption>
      </figure>
    </div>
  </section>
</template>

<style scoped>
.hero-link {
  margin: 1.25rem 0 0;
}
.hero-link a {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  color: var(--on-dark);
  font-weight: 600;
}
.hero-link svg {
  color: var(--blaze);
}
.hero {
  background: var(--hemlock);
  color: var(--on-dark);
  padding: clamp(2rem, 4.5vw, 3.25rem) 0 clamp(2.5rem, 5vw, 3.5rem);
}
.hero-grid {
  display: grid;
  gap: 2.25rem;
}
@media (min-width: 900px) {
  .hero-grid.has-image {
    grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr);
    gap: clamp(2.5rem, 4vw, 4rem);
    align-items: center;
  }
  .has-image .lockup-big {
    font-size: clamp(3rem, 4.9vw, 4.5rem);
  }
}
.hero-photo {
  margin: 0;
}
.hero-photo img {
  display: block;
  width: 100%;
  height: auto;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  border-radius: 10px;
  box-shadow: 0 18px 40px -18px rgba(0, 0, 0, 0.55);
}
.hero-photo figcaption {
  margin-top: 0.6rem;
  font-size: 0.9rem;
  color: var(--on-dark-soft);
}
.lockup {
  margin: 0;
  color: var(--on-dark);
}
.lockup-small {
  display: block;
  font-size: clamp(1.4rem, 3.5vw, 2rem);
  font-weight: 500;
  color: var(--blaze);
  margin-bottom: 0.1em;
}
.lockup-big {
  display: block;
  font-size: clamp(3rem, 11vw, 6.5rem);
  font-weight: 700;
  line-height: 0.95;
  letter-spacing: -0.015em;
}
.tagline {
  margin: 1.25rem 0 0;
  max-width: 34rem;
  font-size: clamp(1.05rem, 2vw, 1.2rem);
  line-height: 1.55;
  color: var(--on-dark-soft);
}
.tagline :deep(p) {
  margin: 0;
  max-width: none;
}
.tagline :deep(p:first-child) {
  font-size: 1.15em;
  color: var(--on-dark);
}
.tagline :deep(p + p) {
  margin-top: 0.85rem;
}
.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1.75rem;
}
</style>
