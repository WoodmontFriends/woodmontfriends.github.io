<template>
  <div class="not-prose card-grid">
    <ContentSlot :use="$slots.default" />
  </div>
</template>

<style scoped>
.card-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr;
  margin: 1.5rem 0;
}
@media (min-width: 600px) {
  .card-grid {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
