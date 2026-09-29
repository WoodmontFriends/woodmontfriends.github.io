<script setup lang="ts">
defineProps({
  primaryLabel: { type: String, default: '' },
  primaryHref: { type: String, default: '' },
  secondaryLabel: { type: String, default: '' },
  secondaryHref: { type: String, default: '' },
})
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
        <a v-if="primaryLabel" :href="primaryHref" class="btn btn-blaze">{{ primaryLabel }}</a>
        <a v-if="secondaryLabel" :href="secondaryHref" class="btn btn-ghost">{{ secondaryLabel }}</a>
      </div>
    </div>
  </section>
</template>

<style scoped>
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
