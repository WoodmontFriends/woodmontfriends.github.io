<script setup lang="ts">
defineProps({
  id: { type: String, default: undefined },
  title: { type: String, required: true },
  tone: { type: String, default: 'paper' }, // 'paper' | 'fern'
})
</script>

<template>
  <section :id="id" class="section" :class="`tone-${tone}`" :aria-labelledby="id ? `${id}-title` : undefined">
    <div class="wrap">
      <div class="layout" :class="{ 'has-aside': $slots.aside }">
        <div class="main-col">
          <h2 :id="id ? `${id}-title` : undefined" class="section-title">{{ title }}</h2>
          <div class="md">
            <ContentSlot :use="$slots.default" />
          </div>
        </div>
        <aside v-if="$slots.aside" class="aside-col">
          <ContentSlot :use="$slots.aside" />
        </aside>
      </div>
    </div>
  </section>
</template>

<style scoped>
.section {
  padding: clamp(3rem, 7vw, 5rem) 0;
  scroll-margin-top: 1rem;
}
.tone-fern {
  background: var(--fern);
}
.section-title {
  font-size: clamp(1.85rem, 4vw, 2.5rem);
  font-weight: 700;
  margin: 0 0 1.25rem;
}
.layout {
  display: grid;
  gap: 2.5rem;
}
@media (min-width: 860px) {
  .layout.has-aside {
    grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr);
    gap: 4rem;
    align-items: start;
  }
}
</style>
