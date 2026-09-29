<script setup lang="ts">
defineProps({
  title: { type: String, required: true },
})
</script>

<template>
  <li class="stop">
    <span class="marker" aria-hidden="true" />
    <h3 class="stop-title">{{ title }}</h3>
    <div class="md">
      <ContentSlot :use="$slots.default" />
    </div>
  </li>
</template>

<style scoped>
.stop {
  position: relative;
  padding: 0 0 2.25rem 2.75rem;
}
.stop:last-child {
  padding-bottom: 0;
}
/* The trail between stops */
.stop::before {
  content: '';
  position: absolute;
  left: 0.6rem;
  top: 0.5rem;
  bottom: -0.5rem;
  border-left: 3px dashed #8fa596;
}
.stop:last-child::before {
  display: none;
}
/* A painted blaze at each stop */
.marker {
  position: absolute;
  left: 0.2rem;
  top: 0.2rem;
  width: 1.05rem;
  height: 1.7rem;
  background: var(--blaze);
  border: 2px solid var(--hemlock);
  border-radius: 2px;
}
.stop-title {
  margin: 0 0 0.35rem;
  font-size: 1.4rem;
  font-weight: 700;
}
</style>
