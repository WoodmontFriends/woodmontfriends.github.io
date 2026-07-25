<template>
  <div class="not-prose fwp-hero">
    <span class="badge">{{ badge }}</span>
    <h1 class="title">Friends of Woodmont Park</h1>
    <p class="tagline"><ContentSlot :use="$slots.default" unwrap="p" /></p>
  </div>
</template>

<script setup lang="ts">
defineProps({
  badge: { type: String, default: 'Coming Soon' },
})
</script>

<style scoped>
.fwp-hero {
  /* Break out of the prose container to full viewport width */
  margin: -2rem calc(50% - 50vw) 2.5rem;
  padding: 4rem 1.25rem 3.25rem;
  text-align: center;
  color: #fff;
  background: linear-gradient(160deg, #1b3a2a, #2d5a40);
}
.badge {
  display: inline-block;
  font-size: 0.8rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.35);
  border-radius: 999px;
  padding: 0.3rem 1rem;
  margin-bottom: 1.25rem;
}
.title {
  font-size: clamp(2rem, 6vw, 3.25rem);
  line-height: 1.15;
  font-weight: 800;
  margin-bottom: 0.75rem;
}
.tagline {
  font-size: clamp(1.05rem, 2.5vw, 1.3rem);
  color: #e8f2ec;
  max-width: 34rem;
  margin: 0 auto;
}
</style>
