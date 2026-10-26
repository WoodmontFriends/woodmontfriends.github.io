<script setup lang="ts">
const props = defineProps({
  primaryLabel: { type: String, default: '' },
  primaryHref: { type: String, default: '' },
  secondaryLabel: { type: String, default: '' },
  secondaryHref: { type: String, default: '' },
  // Optional quiet text link under the buttons, e.g. to the calendar call-out (#calendar).
  linkLabel: { type: String, default: '' },
  linkHref: { type: String, default: '' },
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
    <div class="wrap">
      <h1 class="lockup">
        <span class="lockup-small">Friends of</span>
        <span class="lockup-big">Woodmont Park</span>
      </h1>
      <p class="tagline"><ContentSlot :use="$slots.default" unwrap="p" /></p>
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
  padding: clamp(2.5rem, 7vw, 5rem) 0 clamp(3rem, 8vw, 5.5rem);
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
  margin: 1.5rem 0 0;
  max-width: 34rem;
  font-size: clamp(1.1rem, 2.4vw, 1.3rem);
  line-height: 1.55;
  color: var(--on-dark-soft);
}
.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 2rem;
}
</style>
