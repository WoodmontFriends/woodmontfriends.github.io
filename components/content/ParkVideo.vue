<script setup lang="ts">
// A video with a poster frame and an optional caption. Used for the trail flythrough on /explore.
defineProps({
  src: { type: String, required: true },
  poster: { type: String, default: undefined },
  label: { type: String, required: true },
})
</script>

<template>
  <figure class="park-video">
    <video :src="src" :poster="poster" :aria-label="label" controls playsinline preload="none" />
    <figcaption v-if="$slots.default">
      <ContentSlot :use="$slots.default" unwrap="p" />
    </figcaption>
  </figure>
</template>

<style scoped>
.park-video {
  margin: 1.5rem 0 0;
}
video {
  display: block;
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: 12px;
  background: var(--hemlock);
}
figcaption {
  margin-top: 0.6rem;
  font-size: 0.9rem;
  color: var(--ink-soft);
}
</style>
